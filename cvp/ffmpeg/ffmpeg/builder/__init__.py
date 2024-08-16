# -*- coding: utf-8 -*-

from typing import List

from cvp.ffmpeg.ffmpeg.builder.io import (
    FileBuilder,
    InputFileBuilder,
    OutputFileBuilder,
)


class FFmpegBuilder:
    """
    ffmpeg video converter

    Synopsis:
        ffmpeg [global_options] \
            {[input_file_options] -i input_url} ... \
            {[output_file_options] output_url} ...
    """

    _globals: List[str]
    _files: List[FileBuilder]

    def __init__(self, ffmpeg="ffmpeg") -> None:
        self._ffmpeg = ffmpeg
        self._globals = list()
        self._files = list()

    def append_global_options(self, *args: str):
        self._globals += args
        return self

    def hide_banner(self):
        return self.append_global_options("-hide_banner")

    def infile(self, file: str):
        builder = InputFileBuilder(self, file)
        self._files.append(builder)
        return builder

    def outfile(self, file: str):
        builder = OutputFileBuilder(self, file)
        self._files.append(builder)
        return builder
