# -*- coding: utf-8 -*-

from typing import Final, Sequence

import imgui

_FORCE_READ_ONLY: Final[int] = imgui.INPUT_TEXT_READ_ONLY

DEFAULT_TEXT_COLOR: Final[Sequence[float]] = 0.8, 0.8, 0.8, 1.0
DEFAULT_BACKGROUND_COLOR: Final[Sequence[float]] = 0.2, 0.2, 0.2, 1.0


def input_text_disabled(
    label: str,
    value: str,
    buffer_length=-1,
    flags=0,
    *,
    text_color=DEFAULT_TEXT_COLOR,
    background_color=DEFAULT_BACKGROUND_COLOR,
) -> None:
    imgui.push_item_width(-1)
    imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, *background_color)
    imgui.push_style_color(imgui.COLOR_TEXT, *text_color)
    imgui.input_text(label, value, buffer_length, flags | _FORCE_READ_ONLY)
    imgui.pop_style_color(2)
    imgui.pop_item_width()
