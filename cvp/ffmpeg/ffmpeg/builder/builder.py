# -*- coding: utf-8 -*-

from shlex import join
from typing import List

from cvp.ffmpeg.ffmpeg.builder.global_ import FFmpegGlobalOptions
from cvp.ffmpeg.ffmpeg.builder.io import (
    FileBuilder,
    InputFileBuilder,
    OutputFileBuilder,
)


class FFmpegBuilder(FFmpegGlobalOptions):
    _files: List[FileBuilder]

    def __init__(self, *, ffmpeg="ffmpeg") -> None:
        super().__init__()
        self._ffmpeg = ffmpeg
        self._files = list()

    @property
    def ffmpeg(self):
        return self._ffmpeg

    @ffmpeg.setter
    def ffmpeg(self, value: str) -> None:
        self._ffmpeg = value

    @property
    def files(self):
        return self._files

    def clear(self):
        self._globals.clear()
        self._files.clear()

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

    @property
    def infiles(self) -> List[InputFileBuilder]:
        return [file for file in self._files if isinstance(file, InputFileBuilder)]

    @property
    def outfiles(self) -> List[OutputFileBuilder]:
        return [file for file in self._files if isinstance(file, OutputFileBuilder)]
