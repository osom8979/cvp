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
def get_bin_dir() -> str:
    return os.path.join(get_assets_dir(), "bin")


@lru_cache
def get_fonts_dir() -> str:
    return os.path.join(get_assets_dir(), "fonts")


@lru_cache
def get_cache_dir() -> str:
    return os.path.join(get_assets_dir(), "cache")


def get_assets_path() -> Path:
    return Path(get_assets_dir())


def get_bin_path() -> Path:
    return Path(get_bin_dir())


def get_fonts_path() -> Path:
    return Path(get_fonts_dir())


def get_cache_path() -> Path:
    return Path(get_cache_dir())


@lru_cache
def get_material_design_icons_webfont_ttf() -> str:
    return os.path.join(get_fonts_dir(), "materialdesignicons-webfont.ttf")


@lru_cache
def get_nanum_gothic_coding_ttf() -> str:
    return os.path.join(get_fonts_dir(), "NanumGothicCoding.ttf")


@lru_cache
def get_nanum_gothic_coding_bold_ttf() -> str:
    return os.path.join(get_fonts_dir(), "NanumGothicCoding-Bold.ttf")
