# -*- coding: utf-8 -*-

from typing import Final

import imgui

BACKGROUND_WINDOW_LABEL: Final[str] = "## Background"
BACKGROUND_WINDOW_FLAGS: Final[int] = (
    imgui.WINDOW_NO_DECORATION
    | imgui.WINDOW_NO_SAVED_SETTINGS
    | imgui.WINDOW_NO_FOCUS_ON_APPEARING
    | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS
    | imgui.WINDOW_NO_NAV
    | imgui.WINDOW_NO_MOVE
)


def begin_background(label=BACKGROUND_WINDOW_LABEL):
    viewport = imgui.get_main_viewport()
    pos_x, pos_y = viewport.work_pos
    size_x, size_y = viewport.work_size
    imgui.set_next_window_position(pos_x, pos_y)
    imgui.set_next_window_size(size_x, size_y)

    imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0.0)
    imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
    imgui.begin(label, False, BACKGROUND_WINDOW_FLAGS)
    imgui.pop_style_var(2)


def end_background() -> None:
    imgui.end()
