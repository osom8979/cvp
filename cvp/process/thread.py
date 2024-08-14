# -*- coding: utf-8 -*-

import io
import os
import sys
from abc import ABC, abstractmethod
from functools import lru_cache
from signal import SIGINT
from subprocess import PIPE, Popen
from threading import Thread
from typing import IO, Any, Callable, Mapping, Optional, Sequence, Tuple, Union

from psutil import Process

from cvp.types.override import override


@lru_cache
def default_creation_flags() -> int:
    if sys.platform == "win32":
        from subprocess import CREATE_NO_WINDOW

        return CREATE_NO_WINDOW
    else:
        return 0


class PopenThreadInterface(ABC):
    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError


class PopenThread(PopenThreadInterface):
    def __init__(
        self,
        name: str,
        args: Sequence[Union[str, os.PathLike[str]]],
        buffer_size=io.DEFAULT_BUFFER_SIZE,
        stdin: Optional[Union[int, IO]] = PIPE,
        stdout: Optional[Union[int, IO]] = PIPE,
        stderr: Optional[Union[int, IO]] = PIPE,
        cwd: Optional[Union[str, os.PathLike[str]]] = None,
        env: Optional[Union[Mapping[str, str], Mapping[bytes, bytes]]] = None,
        creation_flags: Optional[int] = None,
        target: Optional[Callable[..., Any]] = None,
    ):
        if creation_flags is None:
            creation_flags = default_creation_flags()

        assert isinstance(creation_flags, int)

        self._process = Popen(
            args,
            bufsize=buffer_size,
            executable=None,
            stdin=stdin,
            stdout=stdout,
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
        self._query = Process(self._process.pid)
        self._thread = Thread(
            group=None,
            target=self.run,
            name=name,
            args=(),
            kwargs=None,
            daemon=None,
        )
        self._target = target

    @override
    def run(self) -> None:
        if self._target is not None:
            self._target()

    @property
    def process(self):
        return self._process

    @property
    def query(self):
        return self._query

    @property
    def thread(self):
        return self._thread

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

    def start(self) -> None:
        self._thread.start()

    def is_alive_thread(self) -> bool:
        return self._thread.is_alive()

    def join_thread(self, timeout: Optional[float] = None) -> None:
        self._thread.join(timeout)

    @property
    def identifier(self):
        return self._thread.ident

    @property
    def native_id(self):
        return self._thread.native_id
