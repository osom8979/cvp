# -*- coding: utf-8 -*-

import os
from collections import OrderedDict
from os import PathLike
from typing import Final, Optional, Union

import imgui

from cvp.assets.fonts import (
    FONT_FILENAME_JBM_NL_NFM_R,
    FONT_FILENAME_MDI,
    FONT_FILENAME_NGC,
    FONT_FILENAME_NGC_B,
)
from cvp.imgui.fonts.builder import FontBuilder
from cvp.imgui.fonts.defaults import (
    add_jbm_font,
    add_mdi_font,
    add_mixed_font,
    add_ngc_b_font,
    add_ngc_font,
)
from cvp.imgui.fonts.font import Font


class FontMapper(OrderedDict[str, Font]):
    __normal_font_name__: Final[str] = "Normal"

    def close(self):
        for font in self.values():
            font.close()

    @staticmethod
    def gen_font_key(name: str, size: int) -> str:
        return f"{name}, {size}px"

    def add_normal_font(self, size: int, *, use_texture=False):
        if self.__contains__(self.__normal_font_name__):
            raise KeyError(f"Already exists font key: {self.__normal_font_name__}")

        font = add_mixed_font(self.__normal_font_name__, size, use_texture=use_texture)
        self.__setitem__(self.__normal_font_name__, font)
        return font

    def add_jbm_font(self, size: int, *, use_texture=False):
        key = self.gen_font_key(FONT_FILENAME_JBM_NL_NFM_R, size)
        if self.__contains__(key):
            raise KeyError(f"Already exists font key: {key}")

        font = add_jbm_font(size, use_texture=use_texture)
        self.__setitem__(key, font)
        return font

    def add_ngc_font(self, size: int, *, use_texture=False):
        key = self.gen_font_key(FONT_FILENAME_NGC, size)
        if self.__contains__(key):
            raise KeyError(f"Already exists font key: {key}")

        font = add_ngc_font(size, use_texture=use_texture)
        self.__setitem__(key, font)
        return font

    def add_ngc_b_font(self, size: int, *, use_texture=False):
        key = self.gen_font_key(FONT_FILENAME_NGC_B, size)
        if self.__contains__(key):
            raise KeyError(f"Already exists font key: {key}")

        font = add_ngc_b_font(size, use_texture=use_texture)
        self.__setitem__(key, font)
        return font

    def add_mdi_font(self, size: int, *, use_texture=False):
        key = self.gen_font_key(FONT_FILENAME_MDI, size)
        if self.__contains__(key):
            raise KeyError(f"Already exists font key: {key}")

        font = add_mdi_font(size, use_texture=use_texture)
        self.__setitem__(key, font)
        return font

    def add_all_fonts(self, size: int, *, use_texture=False):
        self.add_jbm_font(size, use_texture=use_texture)
        self.add_ngc_font(size, use_texture=use_texture)
        self.add_ngc_b_font(size, use_texture=use_texture)
        self.add_mdi_font(size, use_texture=use_texture)

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

    def add_normal_ttf(
        self,
        filepath: Union[str, PathLike[str]],
        size: int,
        *,
        use_texture=False,
    ):
        return self.add_ttf(
            filepath=filepath,
            size=size,
            name=self.__normal_font_name__,
            use_texture=use_texture,
        )

    @staticmethod
    def get_font_global_scale() -> float:
        return imgui.get_io().font_global_scale

    @staticmethod
    def set_font_global_scale(scale: float) -> None:
        imgui.get_io().font_global_scale = scale

    @property
    def normal(self):
        return self.__getitem__(self.__normal_font_name__)
