# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import StrEnum, auto, unique
from typing import List
from uuid import uuid4

from cvp.palette.basic import BLACK, RED, WHITE, YELLOW
from cvp.types.colors import RGB, RGBA
from cvp.types.shapes import ROI


@unique
class Prefix(StrEnum):
    none = ""

    data_type = "&"

    graph_template = "#"
    node_template = "@"
    pin_template = "+"
    arc_template = "~"

    graph = "%"
    node = "$"
    pin = "*"
    arc = "="


@unique
class Action(StrEnum):
    none = auto()
    data = auto()
    flow = auto()


@unique
class Stream(StrEnum):
    input = auto()
    output = auto()


@dataclass
class DataType:
    name: str = field(default_factory=str)  # Primary Key
    docs: str = field(default_factory=str)
    icon: str = field(default_factory=str)
    color: RGBA = field(default_factory=lambda: (*WHITE, 1.0))
    path: str = field(default_factory=str)


@dataclass
class PinTemplate:
    name: str = field(default_factory=str)
    docs: str = field(default_factory=str)
    dtype: str = field(default_factory=str)
    action: Action = field(default_factory=lambda: Action.none)
    stream: Stream = field(default_factory=lambda: Stream.input)
    required: bool = False


@dataclass
class Pin:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default_factory=str)
    docs: str = field(default_factory=str)
    dtype: str = field(default_factory=str)
    action: Action = field(default_factory=lambda: Action.none)
    stream: Stream = field(default_factory=lambda: Stream.input)
    required: bool = False


@dataclass
class ArcTemplate:
    name: str = field(default_factory=str)
    docs: str = field(default_factory=str)
    start_node: str = field(default_factory=str)
    start_pin: str = field(default_factory=str)
    end_node: str = field(default_factory=str)
    end_pin: str = field(default_factory=str)


@dataclass
class Arc:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default_factory=str)
    docs: str = field(default_factory=str)
    start_node: str = field(default_factory=str)
    start_pin: str = field(default_factory=str)
    end_node: str = field(default_factory=str)
    end_pin: str = field(default_factory=str)


@dataclass
class NodeTemplate:
    name: str = field(default_factory=str)
    docs: str = field(default_factory=str)
    icon: str = field(default_factory=str)
    color: RGBA = field(default_factory=lambda: (*WHITE, 1.0))
    pins: List[PinTemplate] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


@dataclass
class NodeState:
    screen_roi: ROI = field(default_factory=lambda: (0.0, 0.0, 0.0, 0.0))
    selected: bool = False
    hovering: bool = False


@dataclass
class Node:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default_factory=str)
    docs: str = field(default_factory=str)
    icon: str = field(default_factory=str)
    roi: ROI = field(default_factory=lambda: (0.0, 0.0, 160.0, 60.0))
    color: RGBA = field(default_factory=lambda: (*WHITE, 1.0))
    pins: List[Pin] = field(default_factory=list)

    _state: NodeState = field(default_factory=NodeState)

    @property
    def state(self) -> NodeState:
        return self._state

    @state.setter
    def state(self, value: NodeState) -> None:
        self._state = value


@dataclass
class GraphTemplate:
    name: str = field(default_factory=str)
    docs: str = field(default_factory=str)
    icon: str = field(default_factory=str)
    color: RGBA = field(default_factory=lambda: (*WHITE, 1.0))
    nodes: List[NodeTemplate] = field(default_factory=list)
    arcs: List[ArcTemplate] = field(default_factory=list)
    dtypes: List[DataType] = field(default_factory=list)


@dataclass
class Canvas:
    pan_x: float = 0.0
    pan_y: float = 0.0
    zoom: float = 1.0


@dataclass
class Grid:
    visible: bool = True
    step: float = 50.0
    thickness: float = 1.0
    color: RGBA = field(default_factory=lambda: (0.8, 0.8, 0.8, 0.2))


@dataclass
class Axis:
    visible: bool = True
    thickness: float = 1.0
    color: RGBA = field(default_factory=lambda: (1.0, 0.0, 0.0, 0.6))


@dataclass
class Stroke:
    color: RGBA = field(default_factory=lambda: (*WHITE, 1.0))
    thickness: float = 1.0
    rounding: float = 1.0
    flags: int = 0

    @classmethod
    def from_rgb(cls, rgb: RGB, thickness=1.0, rounding=1.0, flags=0):
        return cls((rgb[0], rgb[1], rgb[2], 1.0), thickness, rounding, flags)

    @classmethod
    def default_selected(cls):
        return cls.from_rgb(RED, thickness=2.0)

    @classmethod
    def default_hovering(cls):
        return cls.from_rgb(YELLOW, thickness=1.5)

    @classmethod
    def default_normal(cls):
        return cls.from_rgb(WHITE, thickness=1.0)


@dataclass
class Style:
    selected_node: Stroke = field(default_factory=lambda: Stroke.default_selected())
    hovering_node: Stroke = field(default_factory=lambda: Stroke.default_hovering())
    normal_node: Stroke = field(default_factory=lambda: Stroke.default_normal())

    node_name_color: RGBA = field(default_factory=lambda: (*BLACK, 0.8))
    hovering_pin_color: RGBA = field(default_factory=lambda: (*YELLOW, 0.8))

    def get_node_stroke(self, selected=False, hovering=False):
        if selected:
            return self.selected_node
        elif hovering:
            return self.hovering_node
        else:
            return self.normal_node


@dataclass
class Graph:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default_factory=str)
    docs: str = field(default_factory=str)
    icon: str = field(default_factory=str)
    color: RGBA = field(default_factory=lambda: (0.5, 0.5, 0.5, 1.0))
    nodes: List[Node] = field(default_factory=list)
    arcs: List[Arc] = field(default_factory=list)
    dtypes: List[DataType] = field(default_factory=list)
    canvas: Canvas = field(default_factory=Canvas)
    grid_x: Grid = field(default_factory=Grid)
    grid_y: Grid = field(default_factory=Grid)
    axis_x: Axis = field(default_factory=Axis)
    axis_y: Axis = field(default_factory=Axis)
    style: Style = field(default_factory=Style)
