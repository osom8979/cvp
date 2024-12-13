# -*- coding: utf-8 -*-

from enum import IntEnum, unique
from typing import Final

import imgui


@unique
class MouseButton(IntEnum):
    LEFT = imgui.MOUSE_BUTTON_LEFT
    MIDDLE = imgui.MOUSE_BUTTON_MIDDLE
    RIGHT = imgui.MOUSE_BUTTON_RIGHT


MOUSE_LEFT: Final[MouseButton] = MouseButton.LEFT
MOUSE_MIDDLE: Final[MouseButton] = MouseButton.MIDDLE
MOUSE_RIGHT: Final[MouseButton] = MouseButton.RIGHT
