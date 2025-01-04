# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique


@unique
class FontSize(StrEnum):
    normal = auto()
    medium = auto()
    large = auto()
