# -*- coding: utf-8 -*-

from shlex import join, split
from typing import List

from cvp.ffmpeg.ffmpeg.builder.global_ import FFmpegGlobalOptions
from cvp.ffmpeg.ffmpeg.builder.io import (
    FileBuilder,
    InputFileBuilder,
    OutputFileBuilder,
)


class FFmpegBuilder(FFmpegGlobalOptions):
    _files: List[FileBuilder]

    def __init__(
        self,
        *,
        ffmpeg="ffmpeg",
    ) -> None:
        super().__init__()
        self._ffmpeg = ffmpeg
        self._files = list()

    def clear(self):
        self._globals.clear()
        self._files.clear()

    @classmethod
    def from_args(
        cls,
        *args: str,
        ffmpeg="ffmpeg",
    ):
        return cls(ffmpeg=ffmpeg)

    @classmethod
    def from_text(
        cls,
        text: str,
        *,
        comments=False,
        posix=True,
        ffmpeg="ffmpeg",
    ):
        args = split(text, comments=comments, posix=posix)
        return cls.from_args(*args, ffmpeg=ffmpeg)

    def as_args(self) -> List[str]:
        result = list()
        result.extend(self._globals)
        for file in self._files:
            result.extend(file.as_args())
        return result

    def as_text(self):
        return join(self.as_args())

    def append_global_options(self, *args: str):
        self._globals += args
        return self

    def infile(self, file: str):
        builder = InputFileBuilder(self, file)
        self._files.append(builder)
        return builder

    def outfile(self, file: str):
        builder = OutputFileBuilder(self, file)
        self._files.append(builder)
        return builder
