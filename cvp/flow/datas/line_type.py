# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique


@unique
class LineType(StrEnum):
    linear = auto()
    bezier_cubic = auto()
    bezier_quadratic = auto()
