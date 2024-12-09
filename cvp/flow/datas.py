# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import IntEnum, StrEnum, auto, unique
from typing import Final, List
from uuid import uuid4

from cvp.palette.basic import BLACK, RED, WHITE, YELLOW
from cvp.types.colors import RGB, RGBA
from cvp.types.shapes import ROI

_EMPTY_TEXT: Final[str] = ""
_WHITE_RGBA: Final[RGBA] = WHITE[0], WHITE[1], WHITE[2], 1.0
_EMPTY_ROI: Final[ROI] = 0.0, 0.0, 0.0, 0.0
_DEFAULT_NODE_WIDTH: Final[float] = 160.0
_DEFAULT_NODE_HEIGHT: Final[float] = 60.0
_DEFAULT_NODE_ROI: Final[ROI] = 0.0, 0.0, _DEFAULT_NODE_WIDTH, _DEFAULT_NODE_HEIGHT
_DEFAULT_GRID_COLOR: Final[RGBA] = 0.8, 0.8, 0.8, 0.2
_DEFAULT_AXIS_COLOR: Final[RGBA] = 1.0, 0.0, 0.0, 0.6
_DEFAULT_GRAPH_COLOR: Final[RGBA] = 0.5, 0.5, 0.5, 1.0


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


@unique
class IconSize(IntEnum):
    normal = auto()
    medium = auto()
    large = auto()


@dataclass
class DataType:
    name: str = _EMPTY_TEXT  # Primary Key
    docs: str = _EMPTY_TEXT
    icon: str = _EMPTY_TEXT
    color: RGBA = _WHITE_RGBA
    path: str = _EMPTY_TEXT


@dataclass
class PinTemplate:
    name: str = _EMPTY_TEXT
    docs: str = _EMPTY_TEXT
    dtype: str = _EMPTY_TEXT
    action: Action = Action.none
    stream: Stream = Stream.input
    required: bool = False


@dataclass
class Pin:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = _EMPTY_TEXT
    docs: str = _EMPTY_TEXT
    dtype: str = _EMPTY_TEXT
    action: Action = Action.none
    stream: Stream = Stream.input
    required: bool = False


@dataclass
class ArcTemplate:
    name: str = _EMPTY_TEXT
    docs: str = _EMPTY_TEXT
    start_node: str = _EMPTY_TEXT
    start_pin: str = _EMPTY_TEXT
    end_node: str = _EMPTY_TEXT
    end_pin: str = _EMPTY_TEXT


@dataclass
class Arc:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = _EMPTY_TEXT
    docs: str = _EMPTY_TEXT
    start_node: str = _EMPTY_TEXT
    start_pin: str = _EMPTY_TEXT
    end_node: str = _EMPTY_TEXT
    end_pin: str = _EMPTY_TEXT


@dataclass
class NodeTemplate:
    name: str = _EMPTY_TEXT
    docs: str = _EMPTY_TEXT
    icon: str = _EMPTY_TEXT
    color: RGBA = _WHITE_RGBA
    pins: List[PinTemplate] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


@dataclass
class NodeState:
    screen_roi: ROI = _EMPTY_ROI
    selected: bool = False
    hovering: bool = False


@dataclass
class Node:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = _EMPTY_TEXT
    docs: str = _EMPTY_TEXT
    icon: str = _EMPTY_TEXT
    roi: ROI = _DEFAULT_NODE_ROI
    color: RGBA = _WHITE_RGBA
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
    name: str = _EMPTY_TEXT
    docs: str = _EMPTY_TEXT
    icon: str = _EMPTY_TEXT
    color: RGBA = _WHITE_RGBA
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
    color: RGBA = _DEFAULT_GRID_COLOR


@dataclass
class Axis:
    visible: bool = True
    thickness: float = 1.0
    color: RGBA = _DEFAULT_AXIS_COLOR


@dataclass
class Stroke:
    color: RGBA = _WHITE_RGBA
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


@dataclass
class Graph:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = _EMPTY_TEXT
    docs: str = _EMPTY_TEXT
    color: RGBA = _DEFAULT_GRAPH_COLOR
    nodes: List[Node] = field(default_factory=list)
    arcs: List[Arc] = field(default_factory=list)
    dtypes: List[DataType] = field(default_factory=list)
    canvas: Canvas = field(default_factory=Canvas)
    grid_x: Grid = field(default_factory=Grid)
    grid_y: Grid = field(default_factory=Grid)
    axis_x: Axis = field(default_factory=Axis)
    axis_y: Axis = field(default_factory=Axis)
    style: Style = field(default_factory=Style)
