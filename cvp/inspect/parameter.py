# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique


@unique
class ParamType(StrEnum):
    boolean = auto()
    complex = auto()
    floating = auto()
    integer = auto()
    mapping = auto()
    sequence = auto()
    string = auto()
    uri = auto()


class Parameter:
    def __init__(
        self,
        ptype: ParamType,
        name: str,
        value=None,
        min_value=None,
        max_value=None,
    ):
        self._ptype = ptype
        self._name = name
        self._value = value
        self._min_value = min_value
        self._max_value = max_value
