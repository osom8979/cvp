# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Final

from cvp.types.colors import RGBA

DEFAULT_AXIS_COLOR: Final[RGBA] = 1.0, 0.0, 0.0, 0.6


@dataclass
class Axis:
    visible: bool = True
    thickness: float = 1.0
    color: RGBA = DEFAULT_AXIS_COLOR
