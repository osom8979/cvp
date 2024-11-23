# -*- coding: utf-8 -*-

from typing import Sequence

from cvp.fonts.ranges import CodepointRange
from cvp.fonts.ttf import TTF


class CachedTTF:
    def __init__(self, ttf: TTF, ranges: Sequence[CodepointRange], size: int):
        self._ttf = ttf
        self._ranges = list(ranges if ranges else ())
        self._size = size

    @property
    def ttf(self):
        return self._ttf

    @property
    def ranges(self):
        return self._ranges

    @property
    def size(self):
        return self._size

    def has_codepoint(self, codepoint: int) -> bool:
        for begin, end in self._ranges:
            if begin <= codepoint <= end:
                return True
        return False
