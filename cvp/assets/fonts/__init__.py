# -*- coding: utf-8 -*-

import os
from functools import lru_cache
from typing import Final

from cvp.assets import get_assets_dir
from cvp.variables import CODEPOINT_GLYPHS_EXTENSION, CODEPOINT_RANGES_EXTENSION


@lru_cache
def get_fonts_dir() -> str:
    return os.path.join(get_assets_dir(), "fonts")


JBM_DIR: Final[str] = "JetBrainsMono"
MDI_DIR: Final[str] = "MaterialDesignIcons"
NGC_DIR: Final[str] = "NanumGothicCoding"

FONT_FILENAME_JBM_NL_NFM_R: Final[str] = "JetBrainsMonoNLNerdFontMono-Regular"
FONT_FILENAME_MDI: Final[str] = "materialdesignicons-webfont"
FONT_FILENAME_NGC: Final[str] = "NanumGothicCoding"
FONT_FILENAME_NGC_B: Final[str] = "NanumGothicCoding-Bold"

_TTF: Final[str] = ".ttf"
FONT_TTF_FILENAME_JBM_NL_NFM_R: Final[str] = FONT_FILENAME_JBM_NL_NFM_R + _TTF
FONT_TTF_FILENAME_MDI: Final[str] = FONT_FILENAME_MDI + _TTF
FONT_TTF_FILENAME_NGC: Final[str] = FONT_FILENAME_NGC + _TTF
FONT_TTF_FILENAME_NGC_B: Final[str] = FONT_FILENAME_NGC_B + _TTF


@lru_cache
def get_jbm_nl_nfm_r_font_path() -> str:
    return os.path.join(get_fonts_dir(), JBM_DIR, FONT_TTF_FILENAME_JBM_NL_NFM_R)


@lru_cache
def get_mdi_font_path() -> str:
    return os.path.join(get_fonts_dir(), MDI_DIR, FONT_TTF_FILENAME_MDI)


@lru_cache
def get_ngc_font_path() -> str:
    return os.path.join(get_fonts_dir(), NGC_DIR, FONT_TTF_FILENAME_NGC)


@lru_cache
def get_ngc_b_font_path() -> str:
    return os.path.join(get_fonts_dir(), NGC_DIR, FONT_TTF_FILENAME_NGC_B)


_RANGES: Final[str] = CODEPOINT_RANGES_EXTENSION
FONT_RANGES_FILENAME_JBM_NL_NFM_R: Final[str] = FONT_FILENAME_JBM_NL_NFM_R + _RANGES
FONT_RANGES_FILENAME_MDI: Final[str] = FONT_FILENAME_MDI + _RANGES
FONT_RANGES_FILENAME_NGC: Final[str] = FONT_FILENAME_NGC + _RANGES
FONT_RANGES_FILENAME_NGC_B: Final[str] = FONT_FILENAME_NGC_B + _RANGES


@lru_cache
def get_jbm_nl_nfm_r_font_ranges_path() -> str:
    return os.path.join(get_fonts_dir(), JBM_DIR, FONT_RANGES_FILENAME_JBM_NL_NFM_R)


@lru_cache
def get_mdi_font_ranges_path() -> str:
    return os.path.join(get_fonts_dir(), MDI_DIR, FONT_RANGES_FILENAME_MDI)


@lru_cache
def get_ngc_font_ranges_path() -> str:
    return os.path.join(get_fonts_dir(), NGC_DIR, FONT_RANGES_FILENAME_NGC)


@lru_cache
def get_ngc_b_font_ranges_path() -> str:
    return os.path.join(get_fonts_dir(), NGC_DIR, FONT_RANGES_FILENAME_NGC_B)


_GLYPHS: Final[str] = CODEPOINT_GLYPHS_EXTENSION
FONT_GLYPHS_FILENAME_JBM_NL_NFM_R: Final[str] = FONT_FILENAME_JBM_NL_NFM_R + _GLYPHS
FONT_GLYPHS_FILENAME_MDI: Final[str] = FONT_FILENAME_MDI + _GLYPHS
FONT_GLYPHS_FILENAME_NGC: Final[str] = FONT_FILENAME_NGC + _GLYPHS
FONT_GLYPHS_FILENAME_NGC_B: Final[str] = FONT_FILENAME_NGC_B + _GLYPHS


@lru_cache
def get_jbm_nl_nfm_r_font_glyphs_path() -> str:
    return os.path.join(get_fonts_dir(), JBM_DIR, FONT_GLYPHS_FILENAME_JBM_NL_NFM_R)


@lru_cache
def get_mdi_font_glyphs_path() -> str:
    return os.path.join(get_fonts_dir(), MDI_DIR, FONT_GLYPHS_FILENAME_MDI)


@lru_cache
def get_ngc_font_glyphs_path() -> str:
    return os.path.join(get_fonts_dir(), NGC_DIR, FONT_GLYPHS_FILENAME_NGC)


@lru_cache
def get_ngc_b_font_glyphs_path() -> str:
    return os.path.join(get_fonts_dir(), NGC_DIR, FONT_GLYPHS_FILENAME_NGC_B)
