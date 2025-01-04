# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.types.colors import RGBA
from cvp.variables import FLOW_AXIS_COLOR, FLOW_AXIS_THICKNESS, FLOW_AXIS_VISIBLE


@dataclass
class Axis:
    visible: bool = FLOW_AXIS_VISIBLE
    thickness: float = FLOW_AXIS_THICKNESS
    color: RGBA = FLOW_AXIS_COLOR
