# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Final

from cvp.fonts.glyphs.mdi import (
    MDI_ARROW_RIGHT_BOLD,
    MDI_ARROW_RIGHT_BOLD_OUTLINE,
    MDI_CIRCLE,
    MDI_CIRCLE_OUTLINE,
)

FLOW_PIN_N_ICON: Final[str] = MDI_ARROW_RIGHT_BOLD_OUTLINE
FLOW_PIN_Y_ICON: Final[str] = MDI_ARROW_RIGHT_BOLD

DATA_PIN_N_ICON: Final[str] = MDI_CIRCLE_OUTLINE
DATA_PIN_Y_ICON: Final[str] = MDI_CIRCLE


@dataclass
class Pins:
    flow_n_icon: str = FLOW_PIN_N_ICON
    flow_y_icon: str = FLOW_PIN_Y_ICON

    data_n_icon: str = DATA_PIN_N_ICON
    data_y_icon: str = DATA_PIN_Y_ICON
