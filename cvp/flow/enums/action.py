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
class FlowAction(IntEnum):
    flow = 0
    data = 1


FLOW_ACTION_FLOW: Final[int] = FlowAction.flow.value
FLOW_ACTION_DATA: Final[int] = FlowAction.flow.value

DEFAULT_FLOW_ACTION: Final[FlowAction] = FlowAction.flow
DEFAULT_FLOW_ACTION_VALUE: Final[int] = DEFAULT_FLOW_ACTION.value
DEFAULT_FLOW_ACTION_NAME: Final[str] = DEFAULT_FLOW_ACTION.name

FLOW_ACTION_NAME2INDEX: Final[FrozenNameToNumber] = name2number(FlowAction)
FLOW_ACTION_INDEX2NAME: Final[FrozenNumberToName] = number2name(FlowAction)


def normalize_action_value(value: Optional[Union[FlowAction, str, int]]) -> int:
    if value is None:
        return DEFAULT_FLOW_ACTION_VALUE
    return normalize_name2number(FLOW_ACTION_NAME2INDEX, value)


def normalize_action_name(value: Optional[Union[FlowAction, str, int]]) -> str:
    if value is None:
        return DEFAULT_FLOW_ACTION_NAME
    return normalize_number2name(FLOW_ACTION_INDEX2NAME, value)
