# -*- coding: utf-8 -*-

from enum import StrEnum, unique
from typing import Final, Optional, Union

PATH_SEPARATOR: Final[str] = "."
PATH_ENCODING: Final[str] = "utf-8"


def remove_suffix_separators(path: str) -> str:
    if path.endswith(PATH_SEPARATOR):
        return remove_suffix_separators(path[:-1])
    else:
        return path


@unique
class FlowPathPrefixes(StrEnum):
    graph = "#"
    node = "@"
    pin = "+"
    arc = "~"

    graph_instance = "%"
    node_instance = "$"
    pin_instance = "*"
    arc_instance = "="

    reference = "&"


class FlowPath:
    Prefixes = FlowPathPrefixes

    def __init__(self, path: str, *, prefix: Optional[FlowPathPrefixes] = None):
        self._path = str(prefix) + path if prefix else path
        self._data = self._path.encode(PATH_ENCODING)

    def __repr__(self):
        return f"<{type(self).__name__} @{id(self)} path='{self._path}'>"

    def __str__(self):
        return self._path

    def __bytes__(self):
        return self._data

    def __format__(self, format_spec):
        return self._path

    def __hash__(self):
        return hash(self._path)

    def __eq__(self, other):
        return isinstance(other, FlowPath) and self._path == other._path

    def normalize(self):
        return type(self)(remove_suffix_separators(self._path))

    def join(self, path: Union["FlowPath", str]):
        return type(self)(
            remove_suffix_separators(self._path)
            + PATH_SEPARATOR
            + remove_suffix_separators(str(path))
        )
