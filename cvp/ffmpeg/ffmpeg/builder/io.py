# -*- coding: utf-8 -*-

from shlex import split
from typing import List

from cvp.types.override import override


class FileBuilder:
    _options: List[str]

    def __init__(self, base, file: str):
        self._base = base
        self._options = list()
        self._file = file
        self._done = False

    def clear(self) -> None:
        self._options.clear()
        self._done = False

    def append(self, *args: str):
        if self._done:
            raise ValueError("The 'done' flag is already set")

        self._options += args
        return self

    def append_with_text(self, text: str, *, comments=False, posix=True):
        return self.append(*split(text, comments=comments, posix=posix))

    def done(self):
        self._done = True

        # [IMPORTANT] Avoid 'circular import' issues
        from cvp.ffmpeg.ffmpeg.builder import FFmpegBuilder

        assert isinstance(self._base, FFmpegBuilder)
        return self._base

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
