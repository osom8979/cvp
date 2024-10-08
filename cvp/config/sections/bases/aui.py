# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.config.sections.bases.window import WindowConfig
from cvp.variables import MIN_SIDEBAR_HEIGHT, MIN_SIDEBAR_WIDTH


@dataclass
class AuiWindowConfig(WindowConfig):
    """Advanced User Interface"""

    split_left: float = MIN_SIDEBAR_WIDTH
    split_right: float = MIN_SIDEBAR_WIDTH
    split_bottom: float = MIN_SIDEBAR_HEIGHT
