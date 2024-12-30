# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.flow.datas.constants import EMPTY_POINT
from cvp.types.shapes import Point


@dataclass
class Anchor:
    pos: Point = EMPTY_POINT

    _selected: bool = False
    _hovering: bool = False

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
