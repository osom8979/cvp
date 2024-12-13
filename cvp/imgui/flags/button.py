# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from typing import Final

import imgui


@unique
class ButtonFlags(IntFlag):
    MOUSE_BUTTON_LEFT = imgui.BUTTON_MOUSE_BUTTON_LEFT
    MOUSE_BUTTON_MIDDLE = imgui.BUTTON_MOUSE_BUTTON_MIDDLE
    MOUSE_BUTTON_RIGHT = imgui.BUTTON_MOUSE_BUTTON_RIGHT


LBUTTON_FLAGS: Final[ButtonFlags] = ButtonFlags.MOUSE_BUTTON_LEFT
MBUTTON_FLAGS: Final[ButtonFlags] = ButtonFlags.MOUSE_BUTTON_MIDDLE
RBUTTON_FLAGS: Final[ButtonFlags] = ButtonFlags.MOUSE_BUTTON_RIGHT
ABUTTON_FLAGS: Final[ButtonFlags] = LBUTTON_FLAGS | MBUTTON_FLAGS | RBUTTON_FLAGS
