# -*- coding: utf-8 -*-

import io
import os
from signal import SIGINT
from subprocess import PIPE
from typing import IO, Dict, Mapping, Optional, Sequence, Tuple, Union

from cvp.ffmpeg.ffmpeg.process import FFmpegProcess


class ProcessMapper(Dict[str, FFmpegProcess]):
    def spawn(
        self,
        key: str,
        args: Sequence[str],
        frame_size: int,
        buffer_size=io.DEFAULT_BUFFER_SIZE,
        stdin: Optional[Union[int, IO]] = PIPE,
        stderr: Optional[Union[int, IO]] = PIPE,
        cwd: Optional[Union[str, os.PathLike[str]]] = None,
        env: Optional[Union[Mapping[str, str], Mapping[bytes, bytes]]] = None,
    ) -> FFmpegProcess:
        if self.__contains__(key):
            raise KeyError(f"Key '{key}' already exists")
        proc = FFmpegProcess(
            name=key,
            args=args,
            frame_size=frame_size,
            buffer_size=buffer_size,
            stdin=stdin,
            stderr=stderr,
            cwd=cwd,
            env=env,
            creation_flags=None,
        )
        self.__setitem__(key, proc)
        return proc

    def pid(self, key: str) -> int:
        return self.__getitem__(key).pid

    def pids(self):
        return {key: proc.pid for key, proc in self.items()}

    def psutil(self, key: str):
        return self.__getitem__(key).psutil

    def returncode(self, key: str) -> int:
        return self.__getitem__(key).returncode

    def stdin(self, key: str):
        return self.__getitem__(key).stdin

    def stdout(self, key: str):
        return self.__getitem__(key).stdout

    def stderr(self, key: str):
        return self.__getitem__(key).stderr

    def args(self, key: str):
        return self.__getitem__(key).args

    def poll(self, key: str) -> Optional[int]:
        return self.__getitem__(key).poll()

    def polls(self):
        return {key: proc.poll() for key, proc in self.items()}

    def wait(self, key: str, timeout: Optional[float] = None) -> int:
        return self.__getitem__(key).wait(timeout)

    def waits(self, timeout: Optional[float] = None):
        return {key: proc.wait(timeout) for key, proc in self.items()}

    def communicate(
        self,
        key: str,
        data: Optional[bytes] = None,
        timeout: Optional[float] = None,
    ) -> Tuple[Optional[bytes], Optional[bytes]]:
        # [WARNING]
        # The data read is buffered in memory,
        # so do not use this method if the data size is large or unlimited.
        stdout, stderr = self.__getitem__(key).communicate(data, timeout)
        assert isinstance(stdout, (type(None), bytes))
        assert isinstance(stderr, (type(None), bytes))
        return stdout, stderr

    def send_signal(self, key: str, signum: int) -> None:
        self.__getitem__(key).send_signal(signum)

    def interrupt(self, key: str) -> None:
        self.__getitem__(key).send_signal(SIGINT)

    def interrupts(self) -> None:
        for proc in self.values():
            proc.send_signal(SIGINT)

    def terminate(self, key: str) -> None:
        self.__getitem__(key).terminate()

    def kill(self, key: str) -> None:
        self.__getitem__(key).kill()
