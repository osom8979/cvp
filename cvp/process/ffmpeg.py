# -*- coding: utf-8 -*-

import io
import os
import sys
from abc import ABC, abstractmethod
from functools import lru_cache
from signal import SIGINT
from subprocess import DEVNULL, PIPE, Popen
from threading import Thread
from typing import IO, Callable, Mapping, Optional, Sequence, Tuple, Union

from psutil import Process

from cvp.types.override import override


@lru_cache
def default_creation_flags() -> int:
    if sys.platform == "win32":
        from subprocess import CREATE_NO_WINDOW

        return CREATE_NO_WINDOW
    else:
        return 0


class FFmpegFrameInterface(ABC):
    @abstractmethod
    def on_frame(self, data: bytes) -> None:
        raise NotImplementedError


class FFmpegFrameReader(FFmpegFrameInterface):
    _remain: Optional[bytes]

    def __init__(self, pipe: IO[bytes], frame_size: int):
        self._pipe = pipe
        self._frame_size = frame_size
        self._remain = None

    @property
    def frame_size(self):
        return self._frame_size

    def flush(self) -> None:
        self._pipe.flush()

    def read(self) -> None:
        if self._remain:
            next_read_size = self._frame_size - len(self._remain)
            self._remain = self.on_recv(self._remain + self._pipe.read(next_read_size))
        else:
            self._remain = self.on_recv(self._pipe.read(self._frame_size))

    def read_eof(self) -> None:
        if self._remain:
            self.on_recv(self._remain + self._pipe.read())
        else:
            self.on_recv(self._pipe.read())

    def on_recv(self, data: bytes) -> Optional[bytes]:
        if len(data) == 0:
            return None

        if len(data) == self._frame_size:
            self.on_frame(data)
            return None

        assert 0 < len(data) < self._frame_size
        return data

    @override
    def on_frame(self, data: bytes) -> None:
        raise NotImplementedError


class FFmpegProcess:
    def __init__(
        self,
        name: str,
        args: Sequence[Union[str, os.PathLike[str]]],
        frame_size: int,
        buffer_size=io.DEFAULT_BUFFER_SIZE,
        stdin: Optional[Union[int, IO]] = None,
        stderr: Optional[Union[int, IO]] = DEVNULL,
        cwd: Optional[Union[str, os.PathLike[str]]] = None,
        env: Optional[Union[Mapping[str, str], Mapping[bytes, bytes]]] = None,
        creation_flags: Optional[int] = None,
        target: Optional[Callable[[bytes], None]] = None,
    ):
        if creation_flags is None:
            creation_flags = default_creation_flags()

        assert isinstance(creation_flags, int)

        self._process = Popen(
            args,
            bufsize=buffer_size,
            executable=None,
            stdin=stdin,
            stdout=PIPE,
            stderr=stderr,
            preexec_fn=None,
            close_fds=True,
            shell=False,
            cwd=cwd,
            env=env,
            universal_newlines=None,
            startupinfo=None,
            creationflags=creation_flags,
            restore_signals=True,
            start_new_session=False,
            pass_fds=(),
            user=None,
            group=None,
            extra_groups=None,
            encoding=None,
            errors=None,
            text=None,
            umask=-1,
            pipesize=-1,
            process_group=None,
        )
        self._thread = Thread(
            group=None,
            target=self._read_stdout_stream,
            name=name,
            args=(),
            kwargs=None,
            daemon=None,
        )
        self._frame_size = frame_size
        self._target = target

    def _read_stdout_stream(self) -> None:
        stdout_pipe = self._process.stdout
        assert stdout_pipe is not None
        self.read_pipe_stream(stdout_pipe)

    def read_pipe_stream(self, pipe: IO[bytes]) -> None:
        remain: Optional[bytes] = None

        while self._process.poll() is None:
            if remain:
                next_read_size = self._frame_size - len(remain)
                remain = self.on_recv(remain + pipe.read(next_read_size))
            else:
                remain = self.on_recv(pipe.read(self._frame_size))

        pipe.flush()
        if remain:
            self.on_recv(remain + pipe.read())
        else:
            self.on_recv(pipe.read())

    def on_frame(self, data: bytes) -> None:
        if self._target is not None:
            self._target(data)

    @property
    def psutil(self):
        return Process(self._process.pid)

    @property
    def pid(self) -> int:
        return self._process.pid

    @property
    def returncode(self) -> int:
        return self._process.returncode

    @property
    def stdin(self):
        return self._process.stdin

    @property
    def stdout(self):
        return self._process.stdout

    @property
    def stderr(self):
        return self._process.stderr

    @property
    def args(self):
        return self._process.args

    def poll(self) -> Optional[int]:
        return self._process.poll()

    def wait(self, timeout: Optional[float] = None) -> int:
        return self._process.wait(timeout)

    def communicate(
        self,
        data: Optional[bytes] = None,
        timeout: Optional[float] = None,
    ) -> Tuple[Optional[bytes], Optional[bytes]]:
        # [WARNING]
        # The data read is buffered in memory,
        # so do not use this method if the data size is large or unlimited.
        stdout, stderr = self._process.communicate(data, timeout)
        assert isinstance(stdout, (type(None), bytes))
        assert isinstance(stderr, (type(None), bytes))
        return stdout, stderr

    def send_signal(self, signum: int) -> None:
        self._process.send_signal(signum)

    def interrupt(self) -> None:
        self._process.send_signal(SIGINT)

    def terminate(self) -> None:
        self._process.terminate()

    def kill(self) -> None:
        self._process.kill()

    def start_thread(self) -> None:
        self._thread.start()

    def is_alive_thread(self) -> bool:
        return self._thread.is_alive()

    def join_thread(self, timeout: Optional[float] = None) -> None:
        self._thread.join(timeout)

    @property
    def thread_identifier(self):
        return self._thread.ident

    @property
    def thread_native_id(self):
        return self._thread.native_id
