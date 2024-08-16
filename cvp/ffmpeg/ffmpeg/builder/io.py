# -*- coding: utf-8 -*-

from typing import List

from cvp.types.override import override


class FileBuilder:
    _options: List[str]

    def __init__(self, base, file: str):
        self._base = base
        self._options = list()
        self._file = file

    def clear(self) -> None:
        self._options.clear()

    def append(self, *args: str):
        self._options += args
        return self

    def as_args(self) -> List[str]:
        raise NotImplementedError


class InputFileBuilder(FileBuilder):
    @classmethod
    def from_stdin(cls, base):
        return cls(base, "pipe:0")

    @override
    def as_args(self) -> List[str]:
        return self._options + ["-i", self._file]


class OutputFileBuilder(FileBuilder):
    @classmethod
    def from_stdout(cls, base):
        return cls(base, "pipe:1")

    @classmethod
    def from_stderr(cls, base):
        return cls(base, "pipe:2")

    @override
    def as_args(self) -> List[str]:
        return self._options + [self._file]
