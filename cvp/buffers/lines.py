# -*- coding: utf-8 -*-

import os
from collections import deque
from os import PathLike
from typing import BinaryIO, Deque, Optional, Union
from weakref import finalize


def open_file(path: Union[str, PathLike[str]]):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Not found regular file: '{path}'")
    if not os.access(path, os.R_OK):
        raise PermissionError(f"Not readable file: '{path}'")
    return open(path, "rb")


def close_file(f: Optional[BinaryIO]) -> None:
    if f is not None:
        f.close()


class LinesBuffer:
    _lines: Deque[str]
    _file: Optional[BinaryIO]
    _finalizer: Optional[finalize]

    def __init__(
        self,
        path: Union[str, PathLike[str]],
        maxlen: Optional[int] = None,
        encoding="utf-8",
    ):
        self._path = path
        self._encoding = encoding

        self._lines = deque(maxlen=maxlen)
        self._lines.append(str())

        self._file = None
        self._cursor = 0

        self._finalizer = None

    @property
    def path(self):
        return self._path

    @property
    def lines(self):
        return self._lines

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

    def dequeue(self) -> str:
        return self._lines.popleft()

    def enqueue(self, text: str) -> None:
        if not text:
            return

        index = text.find("\n")
        if index >= 0:
            self._lines[-1] += text[0:index]

            next_begin = index + 1
            self._lines.append(str())
            self.enqueue(text[next_begin:])
        else:
            assert index == -1
            self._lines[-1] += text

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
        self.enqueue(str(data, encoding=self._encoding))
        self._cursor = index
        return size

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
