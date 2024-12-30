# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from uuid import uuid4

from cvp.flow.datas.constants import EMPTY_TEXT
from cvp.flow.datas.line_type import LineType
from cvp.flow.datas.node_pin import NodePin
from cvp.types.shapes import Point, Rect


@dataclass
class Arc:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = EMPTY_TEXT
    docs: str = EMPTY_TEXT

    line_type: LineType = LineType.bezier_cubic
    line_args: List[Point] = field(default_factory=list)

    _output: Optional[NodePin] = None
    _input: Optional[NodePin] = None

    _selected: bool = False
    _hovering: bool = False

    _polyline: List[Point] = field(default_factory=list)

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, value: Optional[NodePin]) -> None:
        self._output = value

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, value: Optional[NodePin]) -> None:
        self._input = value

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
    def polyline(self):
        return self._polyline

    @polyline.setter
    def polyline(self, value: List[Point]) -> None:
        self._polyline = value

    def get_polyline_roi(self) -> Rect:
        if not self._polyline:
            raise ValueError("The 'polyline' attribute is empty")

        xs = [p[0] for p in self._polyline]
        ys = [p[1] for p in self._polyline]
        return min(xs), min(ys), max(xs), max(ys)

    def get_bezier_cubic_anchors(self) -> Tuple[Point, Point]:
        if len(self.polyline) < 2:
            raise ValueError("At least 2 'polyline' elements are required")
        if len(self.line_args) < 2:
            raise ValueError("At least 2 'line_args' elements are required")

        # The first/last index point is located at the connected pin.
        sx, sy = self.polyline[0]
        ex, ey = self.polyline[-1]

        sdx, sdy = self.line_args[0]
        edx, edy = self.line_args[1]

        p1 = sx + sdx, sy + sdy
        p2 = ex + edx, ey + edy

        return p1, p2
