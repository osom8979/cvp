# -*- coding: utf-8 -*-

from enum import IntEnum, unique
from typing import Final, Optional, Union

from cvp.types.enum.normalize import (
    FrozenNameToNumber,
    FrozenNumberToName,
    name2number,
    normalize_name2number,
    normalize_number2name,
    number2name,
)


@unique
class FlowStream(IntEnum):
    input = 0
    output = 1


FLOW_STREAM_INPUT: Final[int] = 0
FLOW_STREAM_OUTPUT: Final[int] = 1

DEFAULT_FLOW_STREAM: Final[FlowStream] = FlowStream.input
DEFAULT_FLOW_STREAM_VALUE: Final[int] = DEFAULT_FLOW_STREAM.value
DEFAULT_FLOW_STREAM_NAME: Final[str] = DEFAULT_FLOW_STREAM.name

FLOW_STREAM_NAME2INDEX: Final[FrozenNameToNumber] = name2number(FlowStream)
FLOW_STREAM_INDEX2NAME: Final[FrozenNumberToName] = number2name(FlowStream)


def normalize_stream_value(value: Optional[Union[FlowStream, str, int]]) -> int:
    if value is None:
        return DEFAULT_FLOW_STREAM_VALUE
    return normalize_name2number(FLOW_STREAM_NAME2INDEX, value)


def normalize_stream_name(value: Optional[Union[FlowStream, str, int]]) -> str:
    if value is None:
        return DEFAULT_FLOW_STREAM_NAME
    return normalize_number2name(FLOW_STREAM_INDEX2NAME, value)
