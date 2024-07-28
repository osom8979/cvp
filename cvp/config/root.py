# -*- coding: utf-8 -*-

from enum import IntEnum, StrEnum, auto, unique
from os import PathLike
from typing import Optional, Union

from cvp.config._base import BaseConfig
from cvp.config.sections.display import DisplaySection
from cvp.config.sections.font import FontSection


@unique
class Section(StrEnum):
    DEFAULT = auto()
    font = auto()
    overlay = auto()
    views = auto()
    tools = auto()


@unique
class Key(StrEnum):
    # [DEFAULT]
    open_file_popup_path = auto()

    # [overlay]
    anchor = auto()
    padding = auto()
    alpha = auto()
    fps_warning_threshold = auto()
    fps_error_threshold = auto()

    # [views]
    overlay = auto()

    # [tools]
    demo = auto()


@unique
class Anchor(IntEnum):
    TopLeft = 0
    TopRight = 1
    BottomLeft = 2
    BottomRight = 3


class Config(BaseConfig):
    S = Section
    K = Key

    def __init__(self, filename: Optional[Union[str, PathLike]] = None):
        super().__init__(filename)
        self._display = DisplaySection(self)
        self._font = FontSection(self)

    @property
    def display(self):
        return self._display

    @property
    def font(self):
        return self._font

    @property
    def overlay_anchor(self) -> Anchor:
        return Anchor(self.get(self.S.overlay, self.K.anchor, 0))

    @overlay_anchor.setter
    def overlay_anchor(self, value: Anchor) -> None:
        self.set(self.S.overlay, self.K.anchor, int(value))

    @property
    def overlay_padding(self) -> float:
        return self.get(self.S.overlay, self.K.padding, 10.0)

    @overlay_padding.setter
    def overlay_padding(self, value: float) -> None:
        self.set(self.S.overlay, self.K.padding, value)

    @property
    def overlay_alpha(self) -> float:
        return self.get(self.S.overlay, self.K.alpha, 0.2)

    @overlay_alpha.setter
    def overlay_alpha(self, value: float) -> None:
        self.set(self.S.overlay, self.K.alpha, value)

    @property
    def overlay_fps_warning_threshold(self) -> float:
        return self.get(self.S.overlay, self.K.fps_warning_threshold, 30.0)

    @overlay_fps_warning_threshold.setter
    def overlay_fps_warning_threshold(self, value: float) -> None:
        self.set(self.S.overlay, self.K.fps_warning_threshold, value)

    @property
    def overlay_fps_error_threshold(self) -> float:
        return self.get(self.S.overlay, self.K.fps_error_threshold, 8.0)

    @overlay_fps_error_threshold.setter
    def overlay_fps_error_threshold(self, value: float) -> None:
        self.set(self.S.overlay, self.K.fps_error_threshold, value)

    @property
    def views_overlay(self) -> bool:
        return self.get(self.S.views, self.K.overlay, False)

    @views_overlay.setter
    def views_overlay(self, value: bool) -> None:
        self.set(self.S.views, self.K.overlay, value)

    @property
    def tools_demo(self) -> bool:
        return self.get(self.S.tools, self.K.demo, False)

    @tools_demo.setter
    def tools_demo(self, value: bool) -> None:
        self.set(self.S.tools, self.K.demo, value)
