# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from typing import Final


@unique
class DragType(StrEnum):
    node_type = auto()


DRAG_NODE_TYPE: Final[str] = str(DragType.node_type)
