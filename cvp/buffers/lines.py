# -*- coding: utf-8 -*-

import os
from abc import ABC, abstractmethod
from collections import deque
from io import StringIO
from os import PathLike
from typing import BinaryIO, Deque, Optional, Union
from weakref import finalize

from cvp.types.override import override


def open_file(path: Union[str, PathLike[str]]):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Not found regular file: '{path}'")
    if not os.access(path, os.R_OK):
        raise PermissionError(f"Not readable file: '{path}'")
    return open(path, "rb")


def close_file(f: Optional[BinaryIO]) -> None:
    if f is not None:
        f.close()


class LinesInterface(ABC):
    @abstractmethod
    def getvalue(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def write(self, text: str) -> None:
        raise NotImplementedError


class LinesBase(LinesInterface, ABC):
    _file: Optional[BinaryIO]
    _finalizer: Optional[finalize]

    def __init__(self, path: Union[str, PathLike[str]], encoding="utf-8"):
        self._path = path
        self._encoding = encoding
        self._cursor = 0
        self._file = None
        self._finalizer = None

    @property
    def path(self):
        return self._path

    @property
    def cursor(self):
        return self._cursor

    @property
    def closed(self):
        if self._file is not None:
            return self._file.closed
        else:
            return False

    def open(self) -> None:
        assert self._file is None
        assert self._finalizer is None
        self._file = open_file(self._path)
        self._finalizer = finalize(self, close_file, self._file)

    def close(self) -> None:
        assert self._file is not None
        assert self._finalizer is not None

        if self._finalizer.detach():
            close_file(self._file)

        self._file = None
        self._finalizer = None

    def get_filesize(self) -> int:
        if not os.path.isfile(self._path):
            raise FileNotFoundError(f"Not found regular file: '{self._path}'")
        if not os.access(self._path, os.R_OK):
            raise PermissionError(f"Not readable file: '{self._path}'")

        try:
            return os.path.getsize(self._path)
        except:  # noqa
            return 0

    def update_safe(self) -> int:
        size = self.get_filesize()
        if size <= self._cursor:
            return 0

        if self.closed:
            self.open()

        return self.update_to_index(size)

    def update(self) -> int:
        return self.update_to_index(self.get_filesize())

    def update_to_index(self, index: int) -> int:
        if self.closed:
            raise ValueError("The file is closed")

        if index < self._cursor:
            raise ValueError("'index' must be greater than 'cursor'")

        if self._cursor == index:
            return 0

        size = index - self._cursor
        assert 0 < size
        assert self._file is not None
        data = self._file.read(size)
        self.write(str(data, encoding=self._encoding))
        self._cursor = index
        return size

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class LinesBuffer(LinesBase):
    def __init__(
        self,
        path: Union[str, PathLike[str]],
        encoding="utf-8",
        maxsize: Optional[int] = None,
        newline_size: Optional[int] = None,
        separator="\n",
        zero_width_space="\\",
    ):
        super().__init__(path, encoding)
        self._buffer = str()
        self._maxsize = maxsize
        self._newline_size = newline_size
        self._separator = separator
        self._zero_width_space = zero_width_space

    @staticmethod
    def merge(buffer: str, text: str, maxsize: Optional[int] = None) -> str:
        if maxsize is not None:
            overflow_size = len(buffer) + len(text) - maxsize
            if 0 < overflow_size:
                result = buffer[overflow_size:] + text
            else:
                result = buffer + text
            assert len(result) <= maxsize
            return result
        else:
            return buffer + text

    @property
    def pseudo_suffix(self) -> str:
        return self._zero_width_space + self._separator

    def enqueue_text(self, text: str):
        self._buffer = self.merge(self._buffer, text, self._maxsize)

    @override
    def getvalue(self) -> str:
        return self._buffer

    @override
    def write(self, text: str) -> None:
        if not text:
            return

        if self._newline_size is None:
            self.enqueue_text(text)
            return

        last_line_begin = self._buffer.rfind(self._separator)
        if last_line_begin == -1:
            last_line_size = len(self._buffer)
        else:
            last_line_size = len(self._buffer) - last_line_begin - 1

        remain_line_size = self._newline_size - last_line_size
        assert 0 <= remain_line_size

        if len(text) <= remain_line_size:
            self.enqueue_text(text)
            return

        newline_text_index = text.find(self._separator)
        if newline_text_index == -1:
            text1 = text[:remain_line_size] + self.pseudo_suffix
            text2 = text[remain_line_size:]
            self.enqueue_text(text1)
            self.write(text2)
            return

        additional_line_size = newline_text_index + 1
        text1 = text[:additional_line_size]
        text2 = text[additional_line_size:]

        if additional_line_size <= remain_line_size:
            self.enqueue_text(text1)
        else:
            text1_1 = text1[:remain_line_size] + self.pseudo_suffix
            text1_2 = text1[remain_line_size:]
            self.enqueue_text(text1_1)
            self.write(text1_2)

        self.write(text2)


class LinesDeque(LinesBase):
    _lines: Deque[str]

    def __init__(
        self,
        path: Union[str, PathLike[str]],
        encoding="utf-8",
        maxlen: Optional[int] = None,
        separator="\n",
    ):
        super().__init__(path, encoding)
        self._lines = deque(maxlen=maxlen)
        self._lines.append(str())
        self._separator = separator

    @property
    def lines(self):
        return self._lines

    @override
    def getvalue(self) -> str:
        if len(self._lines) == 0:
            return str()
        if len(self._lines) == 1:
            return self._lines[0]

        assert len(self._lines) >= 2
        buffer = StringIO()
        buffer.write(self._lines[0])
        for i in range(1, len(self._lines)):
            buffer.write(self._separator)
            buffer.write(self._lines[i])
        return buffer.getvalue()

    @override
    def write(self, text: str) -> None:
        if not text:
            return

        index = text.find(self._separator)
        if index >= 0:
            self._lines[-1] += text[0:index]

            next_begin = index + 1
            self._lines.append(str())
            self.write(text[next_begin:])
        else:
            assert index == -1
            self._lines[-1] += text
