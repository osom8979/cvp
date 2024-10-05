# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from typing import Final


@unique
class DragTypes(StrEnum):
    flow_node = auto()


DRAG_FLOW_NODE_TYPE: Final[str] = str(DragTypes.flow_node)
