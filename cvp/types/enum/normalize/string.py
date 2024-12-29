# -*- coding: utf-8 -*-

from enum import StrEnum
from types import MappingProxyType
from typing import Type

FrozenStringToIndex = MappingProxyType[str, int]
FrozenIndexToString = MappingProxyType[int, str]


def string2index(e: Type[StrEnum]) -> FrozenStringToIndex:
    return MappingProxyType({str(x): i for i, x in enumerate(e)})


def index2string(e: Type[StrEnum]) -> FrozenIndexToString:
    return MappingProxyType({i: str(x) for i, x in enumerate(e)})
