# -*- coding: utf-8 -*-

from enum import IntEnum, auto, unique


@unique
class FontSize(IntEnum):
    normal = auto()
    medium = auto()
    large = auto()
