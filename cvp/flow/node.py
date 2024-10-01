# -*- coding: utf-8 -*-

from typing import Iterable, List, Optional

from cvp.flow.pin import FlowPin


class FlowNodeTemplate:
    pins: List[FlowPin]

    def __init__(
        self,
        name: str,
        pins: Optional[Iterable[FlowPin]] = None,
        icon: Optional[str] = None,
        color: Optional[str] = None,
    ):
        self.name = name
        self.pins = list(pins if pins else ())
        self.icon = icon if icon else str()
        self.color = color if color else str()

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, type(self))
            and self.name == other.name
            and self.pins == other.pins
            and self.icon == other.icon
            and self.color == other.color
        )
