# -*- coding: utf-8 -*-

from typing import Final

from cvp.types.colors import RGBA
from cvp.types.shapes import Point, Rect, Size

EMPTY_TEXT: Final[str] = str()
EMPTY_POINT: Final[Point] = 0.0, 0.0
EMPTY_SIZE: Final[Size] = 0.0, 0.0
EMPTY_ROI: Final[Rect] = 0.0, 0.0, 0.0, 0.0
WHITE_RGBA: Final[RGBA] = 1.0, 1.0, 1.0, 1.0

DEFAULT_GRID_COLOR: Final[RGBA] = 0.8, 0.8, 0.8, 0.2
DEFAULT_AXIS_COLOR: Final[RGBA] = 1.0, 0.0, 0.0, 0.6
DEFAULT_GRAPH_COLOR: Final[RGBA] = 0.5, 0.5, 0.5, 1.0
DEFAULT_ITEM_SPACING: Final[Size] = 2.0, 2.0
