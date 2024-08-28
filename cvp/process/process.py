# -*- coding: utf-8 -*-

import io
import os
from signal import SIGINT
from subprocess import DEVNULL, Popen
from typing import IO, Mapping, Optional, Sequence, Tuple, Union

import psutil

from cvp.process.flags import default_creation_flags


class Process:
    def __init__(self, popen: Popen):
        if popen.pid == 0:
            raise ValueError("Invalid process ID")

        self._popen = popen
        self._psutil = psutil.Process(popen.pid)

    @staticmethod
    def popen(
        args: Sequence[str],
        buffer_size=io.DEFAULT_BUFFER_SIZE,
        stdin: Optional[Union[int, IO]] = None,
        stdout: Optional[Union[int, IO]] = DEVNULL,
        stderr: Optional[Union[int, IO]] = DEVNULL,
        cwd: Optional[Union[str, os.PathLike[str]]] = None,
        env: Optional[Union[Mapping[str, str], Mapping[bytes, bytes]]] = None,
        creation_flags: Optional[int] = None,
    ):
        if creation_flags is None:
            creation_flags = default_creation_flags()

        assert isinstance(creation_flags, int)

        return Popen(
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

    @property
    def psutil(self):
        return self._psutil

    @property
    def pid(self) -> int:
        return self._popen.pid

    @property
    def returncode(self) -> int:
        return self._popen.returncode

    @property
    def stdin(self):
        return self._popen.stdin

    @property
    def stdout(self):
        return self._popen.stdout

    @property
    def stderr(self):
        return self._popen.stderr

    @property
    def args(self):
        return self._popen.args

    def poll(self) -> Optional[int]:
        return self._popen.poll()

    def wait(self, timeout: Optional[float] = None) -> int:
        return self._popen.wait(timeout)

    def communicate(
        self,
        data: Optional[bytes] = None,
        timeout: Optional[float] = None,
    ) -> Tuple[Optional[bytes], Optional[bytes]]:
        # [WARNING]
        # The data read is buffered in memory,
        # so do not use this method if the data size is large or unlimited.
        stdout, stderr = self._popen.communicate(data, timeout)
        assert isinstance(stdout, (type(None), bytes))
        assert isinstance(stderr, (type(None), bytes))
        return stdout, stderr

    def send_signal(self, signum: int) -> None:
        self._popen.send_signal(signum)

    def interrupt(self) -> None:
        self._popen.send_signal(SIGINT)

    def terminate(self) -> None:
        self._popen.terminate()

    def kill(self) -> None:
        self._popen.kill()
