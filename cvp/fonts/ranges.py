# -*- coding: utf-8 -*-

from os import PathLike
from typing import Final, List, NamedTuple, Sequence, SupportsIndex, Union

HEXADECIMAL: Final[SupportsIndex] = 16
COMMENT_PREFIX: Final[str] = "#"


class CodepointRange(NamedTuple):
    begin: int
    end: int

    def size(self) -> int:
        return abs(self.end - self.begin) + 1


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
