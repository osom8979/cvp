# -*- coding: utf-8 -*-

from cvp.assets.fonts import (
    get_jbm_nl_nfm_r_font_path,
    get_mdi_font_path,
    get_ngc_b_font_path,
    get_ngc_font_path,
)
from cvp.imgui.fonts.builder import FontBuilder
from cvp.imgui.fonts.font import Font


def add_mixed_font(name: str, size: int, ngc_delta=-4, *, use_texture=False) -> Font:
    jbm = get_jbm_nl_nfm_r_font_path()
    ngc = get_ngc_font_path()
    builder = FontBuilder(name, size)
    builder.add_ttf(jbm)
    builder.add_ttf(ngc, size=size + ngc_delta)
    return builder.done(use_texture=use_texture)


def add_jbm_font(name: str, size: int, *, use_texture=False) -> Font:
    jbm = get_jbm_nl_nfm_r_font_path()
    builder = FontBuilder(name, size)
    builder.add_ttf(jbm)
    return builder.done(use_texture=use_texture)


def add_mdi_font(name: str, size: int, *, use_texture=False) -> Font:
    mdi = get_mdi_font_path()
    builder = FontBuilder(name, size)
    builder.add_ttf(mdi)
    return builder.done(use_texture=use_texture)


def add_ngc_font(name: str, size: int, *, use_texture=False) -> Font:
    ngc = get_ngc_font_path()
    builder = FontBuilder(name, size)
    builder.add_ttf(ngc)
    return builder.done(use_texture=use_texture)


def add_ngc_b_font(name: str, size: int, *, use_texture=False) -> Font:
    ngc = get_ngc_b_font_path()
    builder = FontBuilder(name, size)
    builder.add_ttf(ngc)
    return builder.done(use_texture=use_texture)
