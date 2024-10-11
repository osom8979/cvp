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
        path = self._path
        end_index = -len(self._separator)
        while path.endswith(self._separator):
            path = path[:end_index]
        return type(self)(path)

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
            raise IndexError("The path cannot be split")

        module = self._path[:index]
        node_begin = index + 1
        node = self._path[node_begin:]
        return self.SplitResult(module, node)

    def get_module(self) -> str:
        return self.split().module

    def get_node(self) -> str:
        return self.split().node
