# -*- coding: utf-8 -*-

import io
import os
import sys
from pathlib import Path
from subprocess import DEVNULL
from typing import IO, Callable, Dict, Mapping, Optional, Sequence, Tuple, Union

from cvp.arguments import CVP_HOME
from cvp.process.frame.reader import FrameReaderProcess, FrameShape


class ProcessManager(Dict[str, FrameReaderProcess]):
    def __init__(
        self,
        home: Optional[str] = None,
        *,
        ffmpeg="ffmpeg",
        ffprobe="ffprobe",
    ):
        super().__init__()
        self._home = Path(home) if home else CVP_HOME
        self._ffmpeg = ffmpeg
        self._ffprobe = ffprobe

    def spawn_with_frame_reader(
        self,
        key: str,
        args: Sequence[str],
        frame_shape: Union[FrameShape | Tuple[int, int, int] | Sequence[int]],
        buffer_size=io.DEFAULT_BUFFER_SIZE,
        stdin: Optional[Union[int, IO]] = None,
        stderr: Optional[Union[int, IO]] = DEVNULL,
        cwd: Optional[Union[str, os.PathLike[str]]] = None,
        env: Optional[Union[Mapping[str, str], Mapping[bytes, bytes]]] = None,
        creation_flags: Optional[int] = None,
        target: Optional[Callable[[bytes], None]] = None,
    ):
        process = FrameReaderProcess.from_args(
            name=key,
            args=args,
            frame_shape=frame_shape,
            buffer_size=buffer_size,
            stdin=stdin,
            stderr=stderr,
            cwd=cwd,
            env=env,
            creation_flags=creation_flags,
            target=target,
        )
        process.start_thread()
        self.__setitem__(key, process)
        return process

    def spawn_with_file(self, key: str, width: int, height: int, file: str):
        args = (
            self._ffmpeg,
            "-hide_banner",
            # "-fflags",
            # "nobuffer",
            # "-fflags",
            # "discardcorrupt",
            # "-flags",
            # "low_delay",
            # "-rtsp_transport",
            # "tcp",
            "-i",
            file,
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            f"{width}x{height}",
            "pipe:1",
        )
        frame_shape = width, height, 3
        return self.spawn_with_frame_reader(
            key,
            args=args,
            stderr=sys.stderr.fileno(),
            frame_shape=frame_shape,
        )

    def spawnable(self, key: str) -> bool:
        return not self.__contains__(key)

    def stoppable(self, key: str) -> bool:
        if not self.__contains__(key):
            return False

        process = self.__getitem__(key)
        return process.poll() is None

    def removable(self, key: str) -> bool:
        if not self.__contains__(key):
            return False

        process = self.__getitem__(key)
        if process.is_alive_thread():
            return False

        return process.poll() is not None

    def status(self, key: str) -> str:
        if not self.__contains__(key):
            return "not-exists"

        process = self.__getitem__(key)
        exit_code = process.poll()
        if exit_code is None:
            return process.psutil.status()

        return f"exited ({exit_code})"

    def interrupt(self, key: str) -> None:
        self.__getitem__(key).interrupt()
