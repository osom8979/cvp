# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Final

from cvp.config.sections.bases.window import WindowConfig
from cvp.palette.basic import FUCHSIA, RED, WHITE
from cvp.types.colors import RGB

DEFAULT_BOARD_WIDTH: Final[int] = 10
DEFAULT_BOARD_HEIGHT: Final[int] = 20


@dataclass
class TetrixWindowConfig(WindowConfig):
    board_width: int = DEFAULT_BOARD_WIDTH
    board_height: int = DEFAULT_BOARD_HEIGHT

    current_block_color: RGB = FUCHSIA
    fixed_block_color: RGB = RED
    outline_color: RGB = WHITE

    high_score: int = 0
