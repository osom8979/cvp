# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List, Optional
from uuid import uuid4

from cvp.flow.datas.constants import EMPTY_POINT, EMPTY_SIZE, EMPTY_TEXT, WHITE_RGBA
from cvp.flow.datas.pin import Pin
from cvp.types.colors import RGBA
from cvp.types.shapes import ROI, Point, Size


@dataclass
class Node:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = EMPTY_TEXT
    docs: str = EMPTY_TEXT
    emblem: str = EMPTY_TEXT
    color: RGBA = WHITE_RGBA

    emblem_pos: Point = EMPTY_POINT
    emblem_size: Size = EMPTY_SIZE

    name_pos: Point = EMPTY_POINT
    name_size: Size = EMPTY_SIZE

    node_pos: Point = EMPTY_POINT
    node_size: Size = EMPTY_SIZE

    flow_inputs: List[Pin] = field(default_factory=list)
    flow_outputs: List[Pin] = field(default_factory=list)

    data_inputs: List[Pin] = field(default_factory=list)
    data_outputs: List[Pin] = field(default_factory=list)

    _selected: bool = False
    _hovering: bool = False

    @property
    def node_roi(self) -> ROI:
        x, y = self.node_pos
        w, h = self.node_size
        return x, y, x + w, y + h

    @node_roi.setter
    def node_roi(self, value: ROI) -> None:
        x1, y1, x2, y2 = value
        self.node_pos = x1, y1
        self.node_size = x2 - x1, y2 - y1

    @property
    def flow_pins(self) -> List[Pin]:
        return self.flow_inputs + self.flow_outputs

    @property
    def data_pins(self) -> List[Pin]:
        return self.data_inputs + self.data_outputs

    @property
    def input_pins(self) -> List[Pin]:
        return self.flow_inputs + self.data_inputs

    @property
    def output_pins(self) -> List[Pin]:
        return self.flow_outputs + self.data_outputs

    @property
    def pins(self) -> List[Pin]:
        return self.flow_pins + self.data_pins

    @property
    def flow_lines(self):
        return max(len(self.flow_inputs), len(self.flow_outputs))

    @property
    def data_lines(self):
        return max(len(self.data_inputs), len(self.data_outputs))

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

    def find_hovering_pin(self) -> Optional[Pin]:
        for pin in self.pins:
            if pin.hovering:
                return pin
        return None

    def find_output_pin(self, arc_uuid: str) -> Optional[Pin]:
        for pin in self.output_pins:
            if arc_uuid in pin.arcs:
                return pin
        return None

    def find_input_pin(self, arc_uuid: str) -> Optional[Pin]:
        for pin in self.input_pins:
            if arc_uuid in pin.arcs:
                return pin
        return None