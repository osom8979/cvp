# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import IntEnum, StrEnum, auto, unique
from typing import Final, List, NamedTuple, Optional, Tuple
from uuid import uuid4

from cvp.fonts.glyphs.mdi import (
    MDI_ARROW_RIGHT_CIRCLE,
    MDI_ARROW_RIGHT_CIRCLE_OUTLINE,
    MDI_CIRCLE,
    MDI_CIRCLE_OUTLINE,
)
from cvp.palette.basic import BLACK, BLUE, RED, SILVER, WHITE
from cvp.palette.tableau import ORANGE
from cvp.types.colors import RGB, RGBA
from cvp.types.shapes import ROI, Point, Size

EMPTY_TEXT: Final[str] = ""
EMPTY_POINT: Final[Point] = 0.0, 0.0
EMPTY_SIZE: Final[Size] = 0.0, 0.0
EMPTY_ROI: Final[ROI] = 0.0, 0.0, 0.0, 0.0

WHITE_RGBA: Final[RGBA] = WHITE[0], WHITE[1], WHITE[2], 1.0
DEFAULT_GRID_COLOR: Final[RGBA] = 0.8, 0.8, 0.8, 0.2
DEFAULT_AXIS_COLOR: Final[RGBA] = 1.0, 0.0, 0.0, 0.6
DEFAULT_GRAPH_COLOR: Final[RGBA] = 0.5, 0.5, 0.5, 1.0
DEFAULT_ITEM_SPACING: Final[Size] = 2.0, 2.0

FLOW_PIN_N_ICON: Final[str] = MDI_ARROW_RIGHT_CIRCLE_OUTLINE
FLOW_PIN_Y_ICON: Final[str] = MDI_ARROW_RIGHT_CIRCLE
DATA_PIN_N_ICON: Final[str] = MDI_CIRCLE_OUTLINE
DATA_PIN_Y_ICON: Final[str] = MDI_CIRCLE


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
    arc = "-"


@unique
class Action(StrEnum):
    data = auto()
    flow = auto()


@unique
class Stream(StrEnum):
    input = auto()
    output = auto()


@unique
class FontSize(IntEnum):
    normal = auto()
    medium = auto()
    large = auto()


@dataclass
class DataType:
    name: str = EMPTY_TEXT
    docs: str = EMPTY_TEXT
    icon: str = EMPTY_TEXT
    color: RGBA = WHITE_RGBA
    path: str = EMPTY_TEXT


@dataclass
class PinTemplate:
    name: str = EMPTY_TEXT
    docs: str = EMPTY_TEXT
    dtype: str = EMPTY_TEXT
    action: Action = Action.data
    stream: Stream = Stream.input
    required: bool = False


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

    _hovering: bool = False

    @property
    def connected(self) -> bool:
        return bool(self.arcs)

    @property
    def icon_roi(self) -> ROI:
        x, y = self.icon_pos
        w, h = self.icon_size
        return x, y, x + w, y + h

    @icon_roi.setter
    def icon_roi(self, value: ROI) -> None:
        x1, y1, x2, y2 = value
        self.icon_pos = x1, y1
        self.icon_size = x2 - x1, y2 - y1

    @property
    def name_roi(self) -> ROI:
        x, y = self.name_pos
        w, h = self.name_size
        return x, y, x + w, y + h

    @name_roi.setter
    def name_roi(self, value: ROI) -> None:
        x1, y1, x2, y2 = value
        self.name_pos = x1, y1
        self.name_size = x2 - x1, y2 - y1

    @property
    def hovering(self):
        return self._hovering

    @hovering.setter
    def hovering(self, value: bool) -> None:
        self._hovering = value


@dataclass
class NodeTemplate:
    name: str = EMPTY_TEXT
    docs: str = EMPTY_TEXT
    emblem: str = EMPTY_TEXT
    color: RGBA = WHITE_RGBA
    pins: List[PinTemplate] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


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

    def find_start_pin(self, arc_uuid: str) -> Optional[Pin]:
        for pin in self.output_pins:
            if arc_uuid in pin.arcs:
                return pin
        return None

    def find_end_pin(self, arc_uuid: str) -> Optional[Pin]:
        for pin in self.input_pins:
            if arc_uuid in pin.arcs:
                return pin
        return None


class NodePin(NamedTuple):
    node: Node
    pin: Pin

    def __str__(self):
        return f"{self.node.name}.{self.pin.name}"


@dataclass
class ArcTemplate:
    start_node: str = EMPTY_TEXT
    start_pin: str = EMPTY_TEXT
    end_node: str = EMPTY_TEXT
    end_pin: str = EMPTY_TEXT


@dataclass
class Arc:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = EMPTY_TEXT
    docs: str = EMPTY_TEXT

    _start: Optional[NodePin] = None
    _end: Optional[NodePin] = None

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value: Optional[NodePin]) -> None:
        self._start = value

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value: Optional[NodePin]) -> None:
        self._end = value


@dataclass
class GraphTemplate:
    name: str = EMPTY_TEXT
    docs: str = EMPTY_TEXT
    icon: str = EMPTY_TEXT
    color: RGBA = WHITE_RGBA
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
    color: RGBA = DEFAULT_GRID_COLOR


@dataclass
class Axis:
    visible: bool = True
    thickness: float = 1.0
    color: RGBA = DEFAULT_AXIS_COLOR


@dataclass
class Stroke:
    color: RGBA = WHITE_RGBA
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
        return cls.from_rgb(ORANGE, thickness=1.5)

    @classmethod
    def default_normal(cls):
        return cls.from_rgb(WHITE, thickness=1.0)


@dataclass
class Style:
    selected_node: Stroke = field(default_factory=lambda: Stroke.default_selected())
    hovering_node: Stroke = field(default_factory=lambda: Stroke.default_hovering())
    normal_node: Stroke = field(default_factory=lambda: Stroke.default_normal())

    normal_color: RGBA = field(default_factory=lambda: (*BLACK, 0.8))
    hovering_color: RGBA = field(default_factory=lambda: (*ORANGE, 0.9))
    layout_color: RGBA = field(default_factory=lambda: (*RED, 0.8))

    pin_connection_color: RGBA = field(default_factory=lambda: (*RED, 0.8))
    pin_connection_thickness: float = 2.0

    selection_box_color: RGBA = field(default_factory=lambda: (*BLUE, 0.3))
    selection_box_thickness: float = 1.0

    arc_color: RGBA = field(default_factory=lambda: (*SILVER, 0.8))
    arc_thickness: float = 2.0

    item_spacing: Size = DEFAULT_ITEM_SPACING

    emblem_size: FontSize = FontSize.large
    title_size: FontSize = FontSize.medium
    text_size: FontSize = FontSize.normal
    icon_size: FontSize = FontSize.normal

    flow_pin_n_icon: str = FLOW_PIN_N_ICON
    flow_pin_y_icon: str = FLOW_PIN_Y_ICON
    data_pin_n_icon: str = DATA_PIN_N_ICON
    data_pin_y_icon: str = DATA_PIN_Y_ICON

    show_layout: bool = False


@dataclass
class Graph:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = EMPTY_TEXT
    docs: str = EMPTY_TEXT
    color: RGBA = DEFAULT_GRAPH_COLOR
    nodes: List[Node] = field(default_factory=list)
    arcs: List[Arc] = field(default_factory=list)
    dtypes: List[DataType] = field(default_factory=list)
    canvas: Canvas = field(default_factory=Canvas)
    grid_x: Grid = field(default_factory=Grid)
    grid_y: Grid = field(default_factory=Grid)
    axis_x: Axis = field(default_factory=Axis)
    axis_y: Axis = field(default_factory=Axis)
    style: Style = field(default_factory=Style)

    def update_nodes_all_unhovering(self) -> None:
        for node in self.nodes:
            node.hovering = False
            for pin in node.pins:
                pin.hovering = False

    def find_hovering_node(self) -> Optional[Node]:
        for node in self.nodes:
            if node.hovering:
                return node
        return None

    def move_selected_nodes(self, delta: Size) -> None:
        dx, dy = delta
        for node in self.nodes:
            if not node.selected:
                continue
            x, y = node.node_pos
            node.node_pos = x + dx, y + dy

    @staticmethod
    def connectable_pins(left: NodePin, right: NodePin) -> bool:
        if left.node == right.node:
            return False
        if left.pin.stream == right.pin.stream:
            return False
        if left.pin.action != left.pin.action:
            return False
        if left.pin.dtype != right.pin.dtype:
            return False
        return True

    @staticmethod
    def reorder_pins(left: NodePin, right: NodePin) -> Tuple[NodePin, NodePin]:
        if left.pin.stream == Stream.input:
            assert right.pin.stream == Stream.output
            return left, right
        else:
            assert left.pin.stream == Stream.output
            assert right.pin.stream == Stream.input
            return right, left

    def _connect_pins(self, in_node_pin: NodePin, out_node_pin: NodePin) -> None:
        in_pin = in_node_pin.pin
        out_pin = out_node_pin.pin
        assert in_pin.stream == Stream.input
        assert out_pin.stream == Stream.output
        if not in_pin.arcs and not out_pin.arcs:
            arc = Arc()
            arc.start = in_node_pin
            arc.end = in_node_pin
            self.arcs.append(arc)
            out_pin.arcs.append(arc.uuid)
            in_pin.arcs.append(arc.uuid)

    def connect_pins(self, left: NodePin, right: NodePin) -> None:
        if not self.connectable_pins(left, right):
            return
        in_node_pin, out_node_pin = self.reorder_pins(left, right)
        in_pin = in_node_pin.pin
        out_pin = out_node_pin.pin
        assert in_pin.stream == Stream.input
        assert out_pin.stream == Stream.output

        if not in_pin.arcs and not out_pin.arcs:
            arc = Arc()
            arc.start = in_node_pin
            arc.end = out_node_pin
            self.arcs.append(arc)
            out_pin.arcs.append(arc.uuid)
            in_pin.arcs.append(arc.uuid)
        elif in_pin.arcs and not out_pin.arcs:
            pass
        elif not in_pin.arcs and out_pin.arcs:
            pass
        elif in_pin.arcs and out_pin.arcs:
            pass
        else:
            assert False, "Inaccessible section"
