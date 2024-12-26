# -*- coding: utf-8 -*-

from enum import IntEnum, unique


@unique
class RelativePosition(IntEnum):
    left = -1
    on = 0
    right = 1
