# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

from cvp.config.sections.bases.window import WindowConfig
from cvp.palette.basic import LIME, RED, WHITE, YELLOW
from cvp.types.colors import RGBA


@dataclass
class ToastWindowConfig(WindowConfig):
    pivot_x: float = 0.5
    pivot_y: float = 1.0
    anchor_x: float = 0.5
    anchor_y: float = 1.0
    margin_x: float = 12.0
    margin_y: float = 12.0
    padding_x: float = 8.0
    padding_y: float = 8.0
    fadein: float = 0.5
    fadeout: float = 0.5
    waiting: float = 2.0
    rounding: float = 15.0
    background_color: RGBA = field(default_factory=lambda: (0.5, 0.5, 0.5, 1.0))
    success_color: RGBA = field(default_factory=lambda: (*LIME, 1.0))
    normal_color: RGBA = field(default_factory=lambda: (*WHITE, 1.0))
    warning_color: RGBA = field(default_factory=lambda: (*YELLOW, 1.0))
    error_color: RGBA = field(default_factory=lambda: (*RED, 1.0))
