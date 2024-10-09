# -*- coding: utf-8 -*-

from typing import Callable, Final, Iterable, TypeVar

_T = TypeVar("_T")

NOT_FOUND_INDEX: Final[int] = -1


def find_index(iterable: Iterable[_T], key: Callable[[_T], bool]) -> int:
    for i, item in enumerate(iterable):
        if key(item):
            return i
    return NOT_FOUND_INDEX
