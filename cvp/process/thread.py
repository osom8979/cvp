# -*- coding: utf-8 -*-

import io
import os
from signal import SIGINT
from subprocess import PIPE, Popen
from threading import Thread
from typing import IO, Mapping, Optional, Sequence, Tuple, Union

from psutil import Process


class PopenThread:
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
    ):
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
            creationflags=0,
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
            target=self._runner,
            name=name,
            args=(),
            kwargs=None,
            daemon=None,
        )
        self._thread.start()

    def _runner(self) -> None:
        pass

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
