# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import StrEnum, auto, unique
from typing import List
from uuid import uuid4

from cvp.palette.basic import WHITE
from cvp.types.colors import RGBA
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
    rounding: float = 0.0
    flags: int = 0
    thickness: float = 2.0
    pins: List[PinTemplate] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


@dataclass
class Node:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default_factory=str)
    docs: str = field(default_factory=str)
    icon: str = field(default_factory=str)
    roi: ROI = field(default_factory=lambda: (0.0, 0.0, 160.0, 60.0))
    color: RGBA = field(default_factory=lambda: (*WHITE, 1.0))
    rounding: float = 1.0
    flags: int = 0
    thickness: float = 2.0
    pins: List[Pin] = field(default_factory=list)


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
    alpha: float = 1.0


@dataclass
class Graph:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default_factory=str)
    docs: str = field(default_factory=str)
    icon: str = field(default_factory=str)
    color: RGBA = field(default_factory=lambda: (*WHITE, 1.0))
    nodes: List[Node] = field(default_factory=list)
    arcs: List[Arc] = field(default_factory=list)
    canvas: Canvas = field(default_factory=Canvas)
