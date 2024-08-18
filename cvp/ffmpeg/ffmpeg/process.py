# -*- coding: utf-8 -*-

import io
import os
import sys
from collections import deque
from functools import lru_cache
from signal import SIGINT
from subprocess import DEVNULL, PIPE, Popen
from threading import Lock, Thread
from typing import (
    IO,
    Callable,
    Deque,
    Mapping,
    NamedTuple,
    Optional,
    Sequence,
    Tuple,
    Union,
)

from psutil import Process

from cvp.ffmpeg.ffmpeg.frames.reader import FFmpegFrameReader
from cvp.types.override import override


class FrameShape(NamedTuple):
    width: int
    height: int
    channels: int

    @property
    def size(self):
        return self.width * self.height * self.channels


@lru_cache
def default_creation_flags() -> int:
    if sys.platform == "win32":
        from subprocess import CREATE_NO_WINDOW

        return CREATE_NO_WINDOW
    else:
        return 0


class FFmpegProcess(FFmpegFrameReader):
    _thread_error: Optional[BaseException]
    _deque: Deque[bytes]

    def __init__(
        self,
        name: str,
        args: Sequence[str],
        frame_shape: Union[FrameShape | Tuple[int, int, int] | Sequence[int]],
        buffer_size=io.DEFAULT_BUFFER_SIZE,
        stdin: Optional[Union[int, IO]] = None,
        stderr: Optional[Union[int, IO]] = DEVNULL,
        cwd: Optional[Union[str, os.PathLike[str]]] = None,
        env: Optional[Union[Mapping[str, str], Mapping[bytes, bytes]]] = None,
        creation_flags: Optional[int] = None,
        *,
        deque_maxsize=2,
        target: Optional[Callable[[bytes], None]] = None,
    ):
        self._thread_error = None
        self._frame_shape = FrameShape(*frame_shape)

        self._deque = deque(maxlen=deque_maxsize)
        self._mutex = Lock()
        self._latest = bytes()
        self._latest_count = 0

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

        assert self._process.pid != 0
        self._psutil = Process(self._process.pid)

        stdout_pipe = self._process.stdout
        assert stdout_pipe is not None

        self._thread = Thread(
            group=None,
            target=self._read_pipe_stream_main,
            name=name,
            args=(),
            kwargs=None,
            daemon=None,
        )

        super().__init__(
            pipe=stdout_pipe,
            frame_size=self._frame_shape.size,
            target=target,
        )

    @property
    def thread_error(self):
        return self._thread_error

    @property
    def frame_shape(self):
        return self._frame_shape

    def raise_if_thread_error(self):
        if self._thread_error is not None:
            raise self._thread_error

    def _read_pipe_stream_main(self) -> None:
        try:
            while self._process.poll() is None:
                self.read()

            self.flush()
            self.read_eof()
        except BaseException as e:
            self._thread_error = e

    @override
    def on_frame(self, data: bytes) -> None:
        if self._target is not None:
            self._target(data)
        else:
            self.enqueue(data)

    def enqueue(self, data: bytes) -> None:
        with self._mutex:
            self._deque.append(data)

    def dequeue(self) -> bytes:
        with self._mutex:
            return self._deque.popleft()

    def dequeue_latest(self) -> bytes:
        try:
            self._latest = self.dequeue()
        except IndexError:
            # pop from an empty deque
            pass
        else:
            self._latest_count += 1

        return self._latest

    @property
    def latest(self):
        return self._latest

    @property
    def latest_count(self):
        return self._latest_count

    @property
    def psutil(self):
        return self._psutil

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
