# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.config.sections.bases.window import WindowConfig
from cvp.variables import (
    AUI_PADDING_HEIGHT,
    AUI_PADDING_WIDTH,
    MAX_SIDEBAR_HEIGHT,
    MAX_SIDEBAR_WIDTH,
    MIN_SIDEBAR_HEIGHT,
    MIN_SIDEBAR_WIDTH,
)


@dataclass
class AuiWindowConfig(WindowConfig):
    """Advanced User Interface"""

    split_left: float = MIN_SIDEBAR_WIDTH
    split_right: float = MIN_SIDEBAR_WIDTH
    split_bottom: float = MIN_SIDEBAR_HEIGHT

    min_sidebar_left: float = MIN_SIDEBAR_WIDTH
    max_sidebar_left: float = MAX_SIDEBAR_WIDTH

    min_sidebar_right: float = MIN_SIDEBAR_WIDTH
    max_sidebar_right: float = MAX_SIDEBAR_WIDTH

    min_sidebar_bottom: float = MIN_SIDEBAR_HEIGHT
    max_sidebar_bottom: float = MAX_SIDEBAR_HEIGHT

    padding_width: float = AUI_PADDING_HEIGHT
    padding_height: float = AUI_PADDING_WIDTH
