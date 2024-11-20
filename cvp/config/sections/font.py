# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Tuple

from cvp.config.sections.bases.manager import ManagerWindowConfig
from cvp.palette.basic import ORANGE, WHITE
from cvp.types.colors import RGBA
from cvp.variables import (
    DEFAULT_API_SELECT_WIDTH,
    MAX_API_SELECT_WIDTH,
    MIN_API_SELECT_WIDTH,
)


@dataclass
class FontConfig:
    family: str = field(default_factory=str)
    scale: float = 1.0
    regular_pixels: int = 14
    icon_pixels: int = 22

    @property
    def regular_font_size_pixels(self):
        return self.regular_pixels * self.scale

    @property
    def icon_font_size_pixels(self):
        return self.icon_pixels * self.scale


@dataclass
class FontManagerConfig(ManagerWindowConfig):
    range_select_width: float = DEFAULT_API_SELECT_WIDTH
    min_range_select_width: float = MIN_API_SELECT_WIDTH
    max_range_select_width: float = MAX_API_SELECT_WIDTH
    selected_block: Tuple[int, int] = field(default_factory=lambda: (0, 0))
    text_color: RGBA = field(default_factory=lambda: (*WHITE, 1.0))
    normal_stroke_color: RGBA = field(default_factory=lambda: (*WHITE, 0.3))
    error_stroke_color: RGBA = field(default_factory=lambda: (*ORANGE, 0.3))
    rounding: float = 0.0
    rect_flags: int = 0
    thickness: float = 1.0
    padding: float = 4.0
