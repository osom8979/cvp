# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

from cvp.palette.basic import BLUE, LIME, MAROON, RED, YELLOW
from cvp.types.colors import RGBA


@dataclass
class Logs:
    filter: str = str()
    autoscroll: bool = False
    lines: int = 100
    level_index: int = 0

    critical_color: RGBA = field(default_factory=lambda: (*MAROON, 1.0))
    error_color: RGBA = field(default_factory=lambda: (*RED, 1.0))
    warning_color: RGBA = field(default_factory=lambda: (*YELLOW, 1.0))
    info_color: RGBA = field(default_factory=lambda: (*LIME, 1.0))
    debug_color: RGBA = field(default_factory=lambda: (*BLUE, 1.0))
