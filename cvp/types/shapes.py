# -*- coding: utf-8 -*-

from typing import Final, Tuple, TypeAlias

_X: TypeAlias = float
_Y: TypeAlias = float

Point: TypeAlias = Tuple[_X, _Y]

_Width: TypeAlias = float
_Height: TypeAlias = float

Size: TypeAlias = Tuple[_Width, _Height]

_X1: TypeAlias = float  # Left
_X2: TypeAlias = float  # Right
_Y1: TypeAlias = float  # Top
_Y2: TypeAlias = float  # Bottom

Rect: TypeAlias = Tuple[_X1, _Y1, _X2, _Y2]

EMPTY_POINT: Final[Point] = 0.0, 0.0
EMPTY_SIZE: Final[Size] = 0.0, 0.0
EMPTY_RECT: Final[Rect] = 0.0, 0.0, 0.0, 0.0

ONE_POINT: Final[Point] = 1.0, 1.0
ONE_SIZE: Final[Size] = 1.0, 1.0
ONE_RECT: Final[Rect] = 1.0, 1.0, 1.0, 1.0
