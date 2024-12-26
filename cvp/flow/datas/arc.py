# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List, Optional
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

    line_type: LineType = LineType.linear
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

    @property
    def polyline_roi(self) -> Optional[Rect]:
        if not self._polyline:
            return None

        xs = [p[0] for p in self._polyline]
        ys = [p[1] for p in self._polyline]
        return min(xs), min(ys), max(xs), max(ys)
