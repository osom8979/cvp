# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from typing import Optional, Union


@unique
class FlowType(StrEnum):
    flow = auto()
    data = auto()


@unique
class FlowStream(StrEnum):
    input = auto()
    output = auto()


class FlowPin:
    def __init__(
        self,
        name: str,
        stream: Union[FlowStream, str],
        ftype: Union[FlowType, str],
        dtype: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[str] = None,
    ):
        self.name = name
        self.stream = str(stream)
        self.ftype = str(ftype)
        self.dtype = dtype if dtype else str()
        self.icon = icon if icon else str()
        self.color = color if color else str()

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, type(self))
            and self.name == other.name
            and self.stream == other.stream
            and self.ftype == other.ftype
            and self.dtype == other.dtype
            and self.icon == other.icon
            and self.color == other.color
        )
