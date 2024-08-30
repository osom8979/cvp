# -*- coding: utf-8 -*-

import sys
from subprocess import DEVNULL
from typing import IO, Final, Mapping, Optional, Sequence, Tuple, Union

from cvp.config.sections.ffmpeg import FFmpegSection
from cvp.process.frame import FrameReaderProcess, FrameShape
from cvp.resources.home import HomeDir

RGB24_CHANNELS: Final[int] = 3


class FFmpegProcessHelper:
    def __init__(
        self,
        section: FFmpegSection,
        home: HomeDir,
    ):
        self._section = section
        self._home = home

    @property
    def ffmpeg(self) -> str:
        return self._section.ffmpeg

    def _spawn(
        self,
        name: str,
        args: Sequence[str],
        frame_shape: Union[FrameShape | Tuple[int, int, int] | Sequence[int]],
        stderr: Optional[Union[int, IO]] = DEVNULL,
        env: Optional[Union[Mapping[str, str], Mapping[bytes, bytes]]] = None,
        start_thread=True,
    ):
        process = FrameReaderProcess(
            name=name,
            args=args,
            frame_shape=frame_shape,
            stdin=None,
            stderr=stderr,
            cwd=self._home,
            env=env,
            creation_flags=None,
            target=None,
        )
        if start_thread:
            process.thread.start()
        return process

    def spawn_with_file(self, key: str, file: str, width: int, height: int):
        args = (
            self.ffmpeg,
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
        frame_shape = width, height, RGB24_CHANNELS
        return self._spawn(
            key,
            args=args,
            stderr=sys.stderr.fileno(),
            frame_shape=frame_shape,
        )
