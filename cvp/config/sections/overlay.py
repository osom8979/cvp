# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import IntEnum, unique
from typing import Tuple

from cvp.config.sections.mixins.window import WindowMixin


@unique
class Anchor(IntEnum):
    TopLeft = 0
    TopRight = 1
    BottomLeft = 2
    BottomRight = 3


@dataclass
class OverlayConfig(WindowMixin):
    anchor: Anchor = Anchor.TopLeft
    padding: float = 10.0
    alpha: float = 0.2
    fps_warning_threshold: float = 30.0
    fps_error_threshold: float = 8.0
    normal_color: Tuple[float, float, float] = 0.0, 1.0, 0.0
    warning_color: Tuple[float, float, float] = 1.0, 1.0, 0.0
    error_color: Tuple[float, float, float] = 1.0, 0.0, 0.0

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
