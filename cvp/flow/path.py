# -*- coding: utf-8 -*-

from typing import Final, NamedTuple, Optional, Union

PATH_SEPARATOR: Final[str] = "."
PATH_ENCODING: Final[str] = "utf-8"


class FlowPath:
    def __init__(
        self,
        path: str,
        *,
        separator: Optional[str] = None,
        encoding: Optional[str] = None,
    ):
        self._path = path
        self._separator = separator if separator else PATH_SEPARATOR
        self._encoding = encoding if encoding else PATH_ENCODING

    def __repr__(self):
        return (
            f"<{type(self).__name__} @{id(self)}"
            f" path='{self._path}'"
            f" separator='{self._separator}'"
            ">"
        )

    def __str__(self):
        return self._path

    def __bytes__(self):
        return self._path.encode(PATH_ENCODING)

    def __format__(self, format_spec):
        return self._path

    def __hash__(self):
        return hash(self._path)

    def __eq__(self, other):
        if isinstance(other, FlowPath):
            return self._path == other._path
        elif isinstance(other, str):
            return self._path == other
        else:
            return self._path == str(other)

    def normalize(self):
        return type(self)(self._path.removesuffix(self._separator))

    def join(self, path: Union["FlowPath", str]):
        return type(self)(
            self._path.removesuffix(self._separator)
            + self._separator
            + str(path).removesuffix(self._separator)
        )

    class SplitResult(NamedTuple):
        module: str
        node: str

    def split(self) -> SplitResult:
        index = self._path.rfind(self._separator)
        if index == -1:
            return self.SplitResult(self._path, str())
        else:
            name_begin = index + 1
            return self.SplitResult(self._path[:index], self._path[name_begin:])

    def get_module(self) -> str:
        return self.split().module

    def get_node(self) -> str:
        return self.split().node
