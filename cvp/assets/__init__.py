# -*- coding: utf-8 -*-

import os
import sys
from functools import lru_cache
from pathlib import Path
from typing import Final

from cvp.variables import CODEPOINT_GLYPHS_EXTENSION, CODEPOINT_RANGES_EXTENSION


@lru_cache
def get_assets_dir() -> str:
    # Check if `_MEIPASS` attribute is available in sys else return current file path
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(getattr(sys, "_MEIPASS"), "assets")
    else:
        return os.path.abspath(os.path.dirname(__file__))


@lru_cache
def get_fonts_dir() -> str:
    return os.path.join(get_assets_dir(), "fonts")


@lru_cache
def get_icons_dir() -> str:
    return os.path.join(get_assets_dir(), "icons")


@lru_cache
def get_wsdl_dir() -> str:
    return os.path.join(get_assets_dir(), "wsdl")


def get_assets_path() -> Path:
    return Path(get_assets_dir())


def get_fonts_path() -> Path:
    return Path(get_fonts_dir())


def get_icons_path() -> Path:
    return Path(get_icons_dir())


def get_wsdl_path() -> Path:
    return Path(get_wsdl_dir())


@lru_cache
def get_default_icon_path() -> str:
    return os.path.join(get_icons_dir(), "icon.png")


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
