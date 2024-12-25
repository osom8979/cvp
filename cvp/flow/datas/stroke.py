# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.flow.datas.constants import WHITE_RGBA
from cvp.palette.basic import RED, WHITE
from cvp.palette.tableau import ORANGE
from cvp.types.colors import RGB, RGBA


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
