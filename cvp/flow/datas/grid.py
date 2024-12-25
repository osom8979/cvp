# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.flow.datas.constants import DEFAULT_GRID_COLOR
from cvp.types.colors import RGBA


@dataclass
class Grid:
    visible: bool = True
    step: float = 50.0
    thickness: float = 1.0
    color: RGBA = DEFAULT_GRID_COLOR
