# -*- coding: utf-8 -*-

import os
from collections import OrderedDict
from dataclasses import dataclass
from os import PathLike
from typing import Optional, Union

import imgui

# noinspection PyProtectedMember
from imgui.core import _Font

from cvp.assets import (
    FONT_FILENAME_JBM_NL_NFM_R,
    FONT_FILENAME_NGC,
    FONT_FILENAME_NGC_B,
)
from cvp.imgui.font import add_jbm_font, add_ngc_b_font, add_ngc_font


@dataclass
class Font:
    font: _Font
    size_pixels: Optional[int] = None

    def __enter__(self):
        imgui.push_font(self.font)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        imgui.pop_font()


class FontMapper(OrderedDict[str, Font]):
    @staticmethod
    def gen_font_key(name: str, size_pixels: int) -> str:
        return f"{name}, {size_pixels}px"

    def add_jbm_font(self, size_pixels: int):
        key = self.gen_font_key(FONT_FILENAME_JBM_NL_NFM_R, size_pixels)
        if self.__contains__(key):
            raise KeyError(f"Already exists font key: {key}")

        font = add_jbm_font(size_pixels)
        result = Font(font, size_pixels)
        self.__setitem__(key, result)
        return result

    def add_ngc_font(self, size_pixels: int):
        key = self.gen_font_key(FONT_FILENAME_NGC, size_pixels)
        if self.__contains__(key):
            raise KeyError(f"Already exists font key: {key}")

        font = add_ngc_font(size_pixels)
        result = Font(font, size_pixels)
        self.__setitem__(key, result)
        return result

    def add_ngc_b_font(self, size_pixels: int):
        key = self.gen_font_key(FONT_FILENAME_NGC_B, size_pixels)
        if self.__contains__(key):
            raise KeyError(f"Already exists font key: {key}")

        font = add_ngc_b_font(size_pixels)
        result = Font(font, size_pixels)
        self.__setitem__(key, result)
        return result

    def add_defaults(self, size_pixels: int) -> None:
        self.add_jbm_font(size_pixels)
        self.add_ngc_font(size_pixels)
        self.add_ngc_b_font(size_pixels)

    def add_korean_ttf(
        self,
        filepath: Union[str, PathLike[str]],
        size_pixels: int,
        *,
        name: Optional[str] = None,
    ):
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"File not found: '{str(filepath)}'")

        io = imgui.get_io()
        korean_ranges = io.fonts.get_glyph_ranges_korean()
        font = io.fonts.add_font_from_file_ttf(filepath, size_pixels, korean_ranges)
        result = Font(font, size_pixels)

        if not name:
            basename = os.path.basename(filepath)
            name, _ = os.path.splitext(basename)
            assert isinstance(name, str)

        self.__setitem__(name, result)
        return result

    @staticmethod
    def get_font_global_scale() -> float:
        return imgui.get_io().font_global_scale

    @staticmethod
    def set_font_global_scale(scale: float) -> None:
        imgui.get_io().font_global_scale = scale
