# -*- coding: utf-8 -*-

from typing import List


class FileBuilder:
    _options: List[str]

    def __init__(self, base, file: str):
        self._base = base
        self._file = file
        self._options = list()

    @classmethod
    def from_stdin(cls, base):
        return cls(base, "pipe:0")

    @classmethod
    def from_stdout(cls, base):
        return cls(base, "pipe:1")

    @classmethod
    def from_stderr(cls, base):
        return cls(base, "pipe:2")

    def append_options(self, *args: str):
        self._options += args
        return self


class InputFileBuilder(FileBuilder):
    pass


class OutputFileBuilder(FileBuilder):
    pass
