# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Final

from cvp.types.colors import RGBA

DEFAULT_GRID_COLOR: Final[RGBA] = 0.8, 0.8, 0.8, 0.2


@dataclass
class Grid:
    visible: bool = True
    step: float = 50.0
    thickness: float = 1.0
    color: RGBA = DEFAULT_GRID_COLOR
