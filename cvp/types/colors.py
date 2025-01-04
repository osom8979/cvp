# -*- coding: utf-8 -*-

from typing import Final, Tuple, TypeAlias

_R: TypeAlias = float
_G: TypeAlias = float
_B: TypeAlias = float
_A: TypeAlias = float

RGB: TypeAlias = Tuple[_R, _G, _B]
RGBA: TypeAlias = Tuple[_R, _G, _B, _A]

# ================
# Grayscale colors
# ================

BLACK_RGB: Final[RGB] = 0.0, 0.0, 0.0
BLACK_RGBA: Final[RGBA] = 0.0, 0.0, 0.0, 1.0

DARK_GRAY_RGB: Final[RGB] = 0.25, 0.25, 0.25
DARK_GRAY_RGBA: Final[RGBA] = 0.25, 0.25, 0.25, 1.0

GRAY_RGB: Final[RGB] = 0.5, 0.5, 0.5
GRAY_RGBA: Final[RGBA] = 0.5, 0.5, 0.5, 1.0

LIGHT_GRAY_RGB: Final[RGB] = 0.75, 0.75, 0.75
LIGHT_GRAY_RGBA: Final[RGBA] = 0.75, 0.75, 0.75, 1.0

WHITE_RGB: Final[RGB] = 1.0, 1.0, 1.0
WHITE_RGBA: Final[RGBA] = 1.0, 1.0, 1.0, 1.0

# ==============
# Primary colors
# ==============

RED_RGB: Final[RGB] = 1.0, 0.0, 0.0
RED_RGBA: Final[RGBA] = 1.0, 0.0, 0.0, 1.0

MEDIUM_RED_RGB: Final[RGB] = 0.5, 0.0, 0.0
MEDIUM_RED_RGBA: Final[RGBA] = 0.5, 0.0, 0.0, 1.0

GREEN_RGB: Final[RGB] = 0.0, 1.0, 0.0
GREEN_RGBA: Final[RGBA] = 0.0, 1.0, 0.0, 1.0

MEDIUM_GREEN_RGB: Final[RGB] = 0.0, 0.5, 0.0
MEDIUM_GREEN_RGBA: Final[RGBA] = 0.0, 0.5, 0.0, 1.0

BLUE_RGB: Final[RGB] = 0.0, 0.0, 1.0
BLUE_RGBA: Final[RGBA] = 0.0, 0.0, 1.0, 1.0

MEDIUM_BLUE_RGB: Final[RGB] = 0.0, 0.0, 0.5
MEDIUM_BLUE_RGBA: Final[RGBA] = 0.0, 0.0, 0.5, 1.0

# ======================
# Secondary colors (1.0)
# ======================

CYAN_RGB: Final[RGB] = 0.0, 1.0, 1.0
CYAN_RGBA: Final[RGBA] = 0.0, 1.0, 1.0, 1.0

MAGENTA_RGB: Final[RGB] = 1.0, 0.0, 1.0
MAGENTA_RGBA: Final[RGBA] = 1.0, 0.0, 1.0, 1.0

YELLOW_RGB: Final[RGB] = 1.0, 1.0, 0.0
YELLOW_RGBA: Final[RGBA] = 1.0, 1.0, 0.0, 1.0

# ======================
# Secondary colors (0.5)
# ======================

TEAL_RGB: Final[RGB] = 0.0, 0.5, 0.5
TEAL_RGBA: Final[RGBA] = 0.0, 0.5, 0.5, 1.0

OLIVE_RGB: Final[RGB] = 0.5, 0.5, 0.0
OLIVE_RGBA: Final[RGBA] = 0.5, 0.5, 0.0, 1.0

PURPLE_RGB: Final[RGB] = 0.5, 0.0, 0.5
PURPLE_RGBA: Final[RGBA] = 0.5, 0.0, 0.5, 1.0
