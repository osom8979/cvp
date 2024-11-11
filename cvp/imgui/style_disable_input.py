# -*- coding: utf-8 -*-

from contextlib import contextmanager
from typing import Final

import imgui

from cvp.types.colors import RGBA

DEFAULT_DISABLE_TEXT_COLOR: Final[RGBA] = 0.8, 0.8, 0.8, 1.0
DEFAULT_DISABLE_BACKGROUND_COLOR: Final[RGBA] = 0.2, 0.2, 0.2, 1.0


@contextmanager
def style_disable_input(
    text_color=DEFAULT_DISABLE_TEXT_COLOR,
    background_color=DEFAULT_DISABLE_BACKGROUND_COLOR,
):
    imgui.push_style_color(imgui.COLOR_TEXT, *text_color)
    imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, *background_color)
    try:
        yield
    finally:
        imgui.pop_style_color(2)
