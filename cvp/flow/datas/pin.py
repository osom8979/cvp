# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List

from cvp.flow.datas.action import Action
from cvp.flow.datas.constants import EMPTY_POINT, EMPTY_SIZE, EMPTY_TEXT
from cvp.flow.datas.stream import Stream
from cvp.types.shapes import Point, Rect, Size


@dataclass
class Pin:
    name: str = EMPTY_TEXT
    docs: str = EMPTY_TEXT
    dtype: str = EMPTY_TEXT
    action: Action = Action.data
    stream: Stream = Stream.input
    required: bool = False

    icon_pos: Point = EMPTY_POINT
    icon_size: Size = EMPTY_SIZE

    name_pos: Point = EMPTY_POINT
    name_size: Size = EMPTY_SIZE

    arcs: List[str] = field(default_factory=list)

    _selected: bool = False
    _hovering: bool = False
    _connectable: bool = False

    @property
    def connected(self) -> bool:
        return bool(self.arcs)

    @property
    def icon_roi(self) -> Rect:
        x, y = self.icon_pos
        w, h = self.icon_size
        return x, y, x + w, y + h

    @icon_roi.setter
    def icon_roi(self, value: Rect) -> None:
        x1, y1, x2, y2 = value
        self.icon_pos = x1, y1
        self.icon_size = x2 - x1, y2 - y1

    @property
    def name_roi(self) -> Rect:
        x, y = self.name_pos
        w, h = self.name_size
        return x, y, x + w, y + h

    @name_roi.setter
    def name_roi(self, value: Rect) -> None:
        x1, y1, x2, y2 = value
        self.name_pos = x1, y1
        self.name_size = x2 - x1, y2 - y1

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value: bool) -> None:
        self._selected = value

    @property
    def hovering(self):
        return self._hovering

    @hovering.setter
    def hovering(self, value: bool) -> None:
        self._hovering = value

    @property
    def connectable(self):
        return self._connectable

    @connectable.setter
    def connectable(self, value: bool) -> None:
        self._connectable = value
