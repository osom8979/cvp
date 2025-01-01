# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

from cvp.config.sections.bases.aui import AuiWindowConfig
from cvp.palette.basic import BLUE, LIME, MAROON, RED, YELLOW
from cvp.types.colors import RGBA
from cvp.variables import MIN_SIDEBAR_HEIGHT


@dataclass
class FlowAuiConfig(AuiWindowConfig):
    split_tree: float = MIN_SIDEBAR_HEIGHT
    min_split_tree: float = MIN_SIDEBAR_HEIGHT

    logs_filter: str = str()
    logs_autoscroll: bool = False
    logs_lines: int = 100
    logs_level_index: int = 0

    logs_critical_color: RGBA = field(default_factory=lambda: (*MAROON, 1.0))
    logs_error_color: RGBA = field(default_factory=lambda: (*RED, 1.0))
    logs_warning_color: RGBA = field(default_factory=lambda: (*YELLOW, 1.0))
    logs_info_color: RGBA = field(default_factory=lambda: (*LIME, 1.0))
    logs_debug_color: RGBA = field(default_factory=lambda: (*BLUE, 1.0))
