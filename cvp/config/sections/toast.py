# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import StrEnum, auto, unique

from cvp.config.sections.bases.window import WindowConfig
from cvp.palette.basic import LIME, RED, WHITE, YELLOW
from cvp.types.colors import RGBA


@unique
class ToastAnchor(StrEnum):
    top_left = auto()
    top_center = auto()
    top_right = auto()
    bottom_left = auto()
    bottom_center = auto()
    bottom_right = auto()


@dataclass
class ToastWindowConfig(WindowConfig):
    anchor: ToastAnchor = ToastAnchor.bottom_center
    padding: float = 10.0
    fadein: float = 1.0
    fadeout: float = 1.0
    success_color: RGBA = field(default_factory=lambda: (*LIME, 1.0))
    normal_color: RGBA = field(default_factory=lambda: (*WHITE, 1.0))
    warning_color: RGBA = field(default_factory=lambda: (*YELLOW, 1.0))
    error_color: RGBA = field(default_factory=lambda: (*RED, 1.0))
