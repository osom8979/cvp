# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import IntEnum, unique

from cvp.config.sections.bases.window import WindowConfig
from cvp.palette.basic import LIME, RED, YELLOW
from cvp.types.colors import RGBA


@unique
class Anchor(IntEnum):
    TopLeft = 0
    TopRight = 1
    BottomLeft = 2
    BottomRight = 3


@dataclass
class OverlayWindowConfig(WindowConfig):
    anchor: Anchor = Anchor.TopLeft
    padding: float = 10.0
    alpha: float = 0.2
    fps_warning_threshold: float = 30.0
    fps_error_threshold: float = 8.0
    error_color: RGBA = field(default_factory=lambda: (*RED, 1.0))
    normal_color: RGBA = field(default_factory=lambda: (*LIME, 1.0))
    warning_color: RGBA = field(default_factory=lambda: (*YELLOW, 1.0))

    @property
    def is_top_left(self):
        return self.anchor == Anchor.TopLeft

    @property
    def is_top_right(self):
        return self.anchor == Anchor.TopRight

    @property
    def is_bottom_left(self):
        return self.anchor == Anchor.BottomLeft

    @property
    def is_bottom_right(self):
        return self.anchor == Anchor.BottomRight

    def set_top_left(self) -> None:
        self.anchor = Anchor.TopLeft

    def set_top_right(self) -> None:
        self.anchor = Anchor.TopRight

    def set_bottom_left(self) -> None:
        self.anchor = Anchor.BottomLeft

    def set_bottom_right(self) -> None:
        self.anchor = Anchor.BottomRight

    @property
    def is_left_side(self):
        return self.anchor in (Anchor.TopLeft, Anchor.BottomLeft)

    @property
    def is_right_side(self):
        return not self.is_left_side

    @property
    def is_top_side(self):
        return self.anchor in (Anchor.TopLeft, Anchor.TopRight)

    @property
    def is_bottom_side(self):
        return not self.is_top_side
