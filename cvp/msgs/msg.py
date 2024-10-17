# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import IntEnum, unique
from typing import Any, Dict, Final, Union
from uuid import uuid4

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


@dataclass
class Msg:
    type: MsgType = MsgType.none
    uuid: str = field(default_factory=lambda: str(uuid4()))
    data: Dict[str, Any] = field(default_factory=dict)

    @property
    def number(self) -> int:
        return get_msg_type_number(self.type)

    @property
    def name(self) -> str:
        return get_msg_type_name(self.type)

    def as_args(self) -> Dict[str, Any]:
        return dict(uuid=self.uuid, **self.data)
