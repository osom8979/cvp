# -*- coding: utf-8 -*-

import os
from collections import OrderedDict
from os import PathLike
from typing import Optional, Union

import imgui

from cvp.assets import (
    FONT_FILENAME_JBM_NL_NFM_R,
    FONT_FILENAME_NGC,
    FONT_FILENAME_NGC_B,
)
from cvp.imgui.font import Font
from cvp.imgui.font_builder import FontBuilder
from cvp.imgui.font_defaults import add_jbm_font, add_ngc_b_font, add_ngc_font


class FontMapper(OrderedDict[str, Font]):
    def close(self):
        for font in self.values():
            font.close()

    @staticmethod
    def gen_font_key(name: str, size: int) -> str:
        return f"{name}, {size}px"

    def add_jbm_font(self, size: int, *, use_texture=False):
        name = FONT_FILENAME_JBM_NL_NFM_R
        key = self.gen_font_key(name, size)
        if self.__contains__(key):
            raise KeyError(f"Already exists font key: {key}")

        font = add_jbm_font(size, use_texture=use_texture)
        self.__setitem__(key, font)
        return font

    def add_ngc_font(self, size: int, *, use_texture=False):
        name = FONT_FILENAME_NGC
        key = self.gen_font_key(name, size)
        if self.__contains__(key):
            raise KeyError(f"Already exists font key: {key}")

        font = add_ngc_font(size, use_texture=use_texture)
        self.__setitem__(key, font)
        return font

    def add_ngc_b_font(self, size: int, *, use_texture=False):
        name = FONT_FILENAME_NGC_B
        key = self.gen_font_key(name, size)
        if self.__contains__(key):
            raise KeyError(f"Already exists font key: {key}")

        font = add_ngc_b_font(size, use_texture=use_texture)
        self.__setitem__(key, font)
        return font

    def add_defaults(self, size: int, *, use_texture=False) -> None:
        self.add_jbm_font(size, use_texture=use_texture)
        self.add_ngc_font(size, use_texture=use_texture)
        self.add_ngc_b_font(size, use_texture=use_texture)

    def add_ttf(
        self,
        filepath: Union[str, PathLike[str]],
        size: int,
        *,
        name: Optional[str] = None,
        use_texture=False,
    ):
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"File not found: '{str(filepath)}'")

        if not name:
            name = os.path.basename(filepath)

        assert isinstance(name, str)

        builder = FontBuilder(name, size)
        builder.add_ttf(filepath)
        font = builder.done(use_texture=use_texture)

        self.__setitem__(name, font)
        return font

    @staticmethod
    def get_font_global_scale() -> float:
        return imgui.get_io().font_global_scale

    @staticmethod
    def set_font_global_scale(scale: float) -> None:
        imgui.get_io().font_global_scale = scale
