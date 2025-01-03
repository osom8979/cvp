# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

from cvp.config.sections.bases.aui import AuiWindowConfig
from cvp.config.sections.flow.arcs import Arcs
from cvp.config.sections.flow.axis import Axis
from cvp.config.sections.flow.grid import Grid
from cvp.config.sections.flow.logs import Logs
from cvp.config.sections.flow.nodes import Nodes
from cvp.config.sections.flow.pins import Pins
from cvp.variables import MIN_SIDEBAR_HEIGHT


@dataclass
class FlowAuiConfig(AuiWindowConfig):
    split_tree: float = MIN_SIDEBAR_HEIGHT
    min_split_tree: float = MIN_SIDEBAR_HEIGHT

    logs: Logs = field(default_factory=Logs)

    grid_x: Grid = field(default_factory=Grid)
    grid_y: Grid = field(default_factory=Grid)

    axis_x: Axis = field(default_factory=Axis)
    axis_y: Axis = field(default_factory=Axis)

    nodes: Nodes = field(default_factory=Nodes)
    arcs: Arcs = field(default_factory=Arcs)
    pins: Pins = field(default_factory=Pins)
