# -*- coding: utf-8 -*-

from typing import Tuple, TypeAlias

_X1: TypeAlias = float  # Left
_X2: TypeAlias = float  # Right

_Y1: TypeAlias = float  # Top
_Y2: TypeAlias = float  # Bottom

ROI: TypeAlias = Tuple[_X1, _Y1, _X2, _Y2]
