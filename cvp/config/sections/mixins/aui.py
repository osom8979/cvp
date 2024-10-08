# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.variables import MIN_SIDEBAR_HEIGHT, MIN_SIDEBAR_WIDTH


@dataclass
class AuiMixin:
    split_left: float = float(MIN_SIDEBAR_WIDTH)
    split_right: float = float(MIN_SIDEBAR_WIDTH)
    split_bottom: float = float(MIN_SIDEBAR_HEIGHT)
