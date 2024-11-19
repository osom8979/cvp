# -*- coding: utf-8 -*-

from os import PathLike
from typing import Final, List, NamedTuple, Sequence, SupportsIndex, Tuple, Union

UNICODE_SINGLE_BLOCK_SIZE: Final[int] = 0x100
COMMENT_PREFIX: Final[str] = "#"
HEXADECIMAL: Final[SupportsIndex] = 16


class CodepointRange(NamedTuple):
    begin: int
    end: int

    def size(self) -> int:
        return abs(self.end - self.begin) + 1

    def has_codepoint(self, codepoint: int) -> bool:
        return self.begin <= codepoint <= self.end

    def as_blocks(self, step=UNICODE_SINGLE_BLOCK_SIZE) -> List[Tuple[int, int]]:
        block_begin = (self.begin // step) * step
        block_end = block_begin + step - 1

        assert block_begin <= self.begin
        result = [(block_begin, block_end)]

        while block_end < self.end:
            block_begin += step
            block_end += step
            result.append((block_begin, block_end))

        return result


def read_ranges(path: Union[str, PathLike[str]]) -> List[CodepointRange]:
    result = list()
    with open(path, "rt") as file:
        for line in file:
            if line and line.startswith(COMMENT_PREFIX):
                continue
            hex_values = line.strip().split()
            assert len(hex_values) == 2
            begin = int(hex_values[0].strip(), HEXADECIMAL)
            end = int(hex_values[1].strip(), HEXADECIMAL)
            result.append(CodepointRange(begin, end))
    return result


def flatten_ranges(ranges: Sequence[CodepointRange]) -> List[int]:
    result = list()
    for begin, end in ranges:
        result.append(begin)
        result.append(end)
    return result
