# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.flow.datas.constants import DEFAULT_AXIS_COLOR
from cvp.types.colors import RGBA


@dataclass
class Axis:
    visible: bool = True
    thickness: float = 1.0
    color: RGBA = DEFAULT_AXIS_COLOR
