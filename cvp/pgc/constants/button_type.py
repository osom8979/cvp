# -*- coding: utf-8 -*-

from enum import IntEnum, unique
from typing import Final

from pygame import constants as pg_constants


@unique
class ButtonType(IntEnum):
    LEFT = pg_constants.BUTTON_LEFT
    MIDDLE = pg_constants.BUTTON_MIDDLE
    RIGHT = pg_constants.BUTTON_RIGHT
    WHEEL_UP = pg_constants.BUTTON_WHEELUP
    WHEEL_DOWN = pg_constants.BUTTON_WHEELDOWN
    X1 = pg_constants.BUTTON_X1
    X2 = pg_constants.BUTTON_X2


BUTTON_MIN: Final[int] = int(ButtonType.LEFT)
BUTTON_MAX: Final[int] = int(ButtonType.X2)
BUTTON_LEN: Final[int] = len(ButtonType)

assert BUTTON_MIN == 1
assert BUTTON_MAX == 7
assert BUTTON_LEN == 7
