# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.types.colors import RGBA
from cvp.variables import (
    FLOW_GRID_COLOR,
    FLOW_GRID_STEP,
    FLOW_GRID_THICKNESS,
    FLOW_GRID_VISIBLE,
)


@dataclass
class Grid:
    visible: bool = FLOW_GRID_VISIBLE
    step: float = FLOW_GRID_STEP
    thickness: float = FLOW_GRID_THICKNESS
    color: RGBA = FLOW_GRID_COLOR
