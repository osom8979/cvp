# -*- coding: utf-8 -*-

from enum import IntEnum, StrEnum, auto, unique
from typing import Tuple

from cvp.assets import get_fonts_path
from cvp.config.base import BaseConfig


@unique
class Section(StrEnum):
    DEFAULT = auto()
    display = auto()
    font = auto()
    overlay = auto()
    views = auto()
    tools = auto()


@unique
class Key(StrEnum):
    # [DEFAULT]
    open_file_popup_path = auto()

    # [display]
    width = auto()
    height = auto()
    fullscreen = auto()
    force_egl = auto()

    # [font]
    family = auto()
    scale = auto()
    pixels = auto()

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

    @property
    def display_width(self) -> int:
        return self.get(self.S.display, self.K.width, -1)

    @display_width.setter
    def display_width(self, value: int) -> None:
        self.set(self.S.display, self.K.width, value)

    @property
    def display_height(self) -> int:
        return self.get(self.S.display, self.K.height, -1)

    @display_height.setter
    def display_height(self, value: int) -> None:
        self.set(self.S.display, self.K.height, value)

    @property
    def display_size(self) -> Tuple[int, int]:
        return self.display_width, self.display_height

    @display_size.setter
    def display_size(self, value: Tuple[int, int]) -> None:
        self.display_width = value[0]
        self.display_height = value[1]

    @property
    def display_fullscreen(self) -> bool:
        return self.get(self.S.display, self.K.fullscreen, False)

    @display_fullscreen.setter
    def display_fullscreen(self, value: bool) -> None:
        self.set(self.S.display, self.K.fullscreen, value)

    @property
    def display_force_egl(self) -> bool:
        return self.get(self.S.display, self.K.force_egl, False)

    @display_force_egl.setter
    def display_force_egl(self, value: bool) -> None:
        self.set(self.S.display, self.K.force_egl, value)

    @property
    def font_family(self) -> str:
        default_font = str(get_fonts_path() / "NanumGothicCoding.ttf")
        return self.get(self.S.font, self.K.family, default_font)

    @font_family.setter
    def font_family(self, value: str) -> None:
        self.set(self.S.font, self.K.family, value)

    @property
    def font_scale(self) -> float:
        return self.get(self.S.font, self.K.scale, 1.0)

    @font_scale.setter
    def font_scale(self, value: float) -> None:
        self.set(self.S.font, self.K.scale, value)

    @property
    def font_pixels(self) -> int:
        return self.get(self.S.font, self.K.pixels, 14)

    @font_pixels.setter
    def font_pixels(self, value: int) -> None:
        self.set(self.S.font, self.K.pixels, value)

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
