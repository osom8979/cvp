# -*- coding: utf-8 -*-

from enum import IntEnum, unique
from typing import Final, Union

from cvp.types.enum.normalize import (
    FrozenNameToNumber,
    FrozenNumberToName,
    name2number,
    normalize_name2number,
    normalize_number2name,
    number2name,
)


@unique
class MsgType(IntEnum):
    none = 0


MSG_TYPE_NAME_TO_NUMBER: Final[FrozenNameToNumber] = name2number(MsgType)
MSG_TYPE_NUMBER_TO_NAME: Final[FrozenNumberToName] = number2name(MsgType)
MsgTypeLike = Union[MsgType, IntEnum, str, int]


def get_msg_type_number(value: MsgTypeLike) -> int:
    return normalize_name2number(MSG_TYPE_NAME_TO_NUMBER, value)


def get_msg_type_name(value: MsgTypeLike) -> str:
    return normalize_number2name(MSG_TYPE_NUMBER_TO_NAME, value)
