# -*- coding: utf-8 -*-

from enum import IntEnum
from types import MappingProxyType
from typing import Type, Union

FrozenNameToNumber = MappingProxyType[str, int]
FrozenNumberToName = MappingProxyType[int, str]
IntEnumLike = Union[IntEnum, str, int]


def name2number(e: Type[IntEnum]) -> FrozenNameToNumber:
    return MappingProxyType({str(x.name): int(x.value) for x in e})


def number2name(e: Type[IntEnum]) -> FrozenNumberToName:
    return MappingProxyType({int(x.value): str(x.name) for x in e})


def normalize_name2number(mapping: FrozenNameToNumber, value: IntEnumLike) -> int:
    if isinstance(value, IntEnum):
        return int(value.value)
    elif isinstance(value, str):
        return mapping[value]
    elif isinstance(value, int):
        return int(value)
    else:
        raise TypeError(f"Unsupported value type: {type(value).__name__}")


def normalize_number2name(mapping: FrozenNumberToName, value: IntEnumLike) -> str:
    if isinstance(value, IntEnum):
        return str(value.name)
    elif isinstance(value, str):
        return str(value)
    elif isinstance(value, int):
        return mapping[value]
    else:
        raise TypeError(f"Unsupported value type: {type(value).__name__}")
