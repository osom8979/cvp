# -*- coding: utf-8 -*-

from enum import IntEnum, StrEnum, auto, unique

from cvp.config._base import BaseConfig
from cvp.config.sections._base import BaseSection


@unique
class Anchor(IntEnum):
    TopLeft = 0
    TopRight = 1
    BottomLeft = 2
    BottomRight = 3


@unique
class _Keys(StrEnum):
    visible = auto()
    anchor = auto()
    padding = auto()
    alpha = auto()
    fps_warning_threshold = auto()
    fps_error_threshold = auto()


class OverlaySection(BaseSection):
    K = _Keys

    def __init__(self, config: BaseConfig):
        super().__init__(config, section="overlay")

    @property
    def visible(self) -> bool:
        return self.get(self.K.visible, False)

    @visible.setter
    def visible(self, value: bool) -> None:
        self.set(self.K.visible, value)

    @property
    def anchor(self) -> Anchor:
        return Anchor(self.get(self.K.anchor, 0))

    @anchor.setter
    def anchor(self, value: Anchor) -> None:
        self.set(self.K.anchor, int(value))

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

    @property
    def padding(self) -> float:
        return self.get(self.K.padding, 10.0)

    @padding.setter
    def padding(self, value: float) -> None:
        self.set(self.K.padding, value)

    @property
    def alpha(self) -> float:
        return self.get(self.K.alpha, 0.2)

    @alpha.setter
    def alpha(self, value: float) -> None:
        self.set(self.K.alpha, value)

    @property
    def fps_warning_threshold(self) -> float:
        return self.get(self.K.fps_warning_threshold, 30.0)

    @fps_warning_threshold.setter
    def fps_warning_threshold(self, value: float) -> None:
        self.set(self.K.fps_warning_threshold, value)

    @property
    def fps_error_threshold(self) -> float:
        return self.get(self.K.fps_error_threshold, 8.0)

    @fps_error_threshold.setter
    def fps_error_threshold(self, value: float) -> None:
        self.set(self.K.fps_error_threshold, value)
