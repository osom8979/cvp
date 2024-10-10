# -*- coding: utf-8 -*-

import os
import sys
from functools import lru_cache
from pathlib import Path


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
def get_jbm_nl_nfm_r_font_path() -> str:
    return os.path.join(get_fonts_dir(), "JetBrainsMonoNLNerdFontMono-Regular.ttf")


@lru_cache
def get_mdi_font_path() -> str:
    return os.path.join(get_fonts_dir(), "materialdesignicons-webfont.ttf")


@lru_cache
def get_ngc_font_path() -> str:
    return os.path.join(get_fonts_dir(), "NanumGothicCoding.ttf")


@lru_cache
def get_ngc_b_font_path() -> str:
    return os.path.join(get_fonts_dir(), "NanumGothicCoding-Bold.ttf")


@lru_cache
def get_default_icon_path() -> str:
    return os.path.join(get_icons_dir(), "icon.png")
