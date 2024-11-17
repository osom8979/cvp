# -*- coding: utf-8 -*-

import os

from cvp.assets import (
    get_jbm_nl_nfm_r_font_path,
    get_mdi_font_path,
    get_ngc_b_font_path,
    get_ngc_font_path,
)
from cvp.imgui.font import Font
from cvp.imgui.font_builder import FontBuilder


def add_ngc_font(size: int, mdi_delta=0, *, use_texture=False) -> Font:
    ngc = get_ngc_font_path()
    mdi = get_mdi_font_path()
    basename = os.path.basename(ngc)
    builder = FontBuilder(basename, size)
    builder.add_ttf(ngc)
    builder.add_ttf(mdi, size=size + mdi_delta)
    return builder.done(use_texture=use_texture)


def add_ngc_b_font(size: int, mdi_delta=0, *, use_texture=False) -> Font:
    ngc = get_ngc_b_font_path()
    mdi = get_mdi_font_path()
    basename = os.path.basename(ngc)
    builder = FontBuilder(basename, size)
    builder.add_ttf(ngc)
    builder.add_ttf(mdi, size=size + mdi_delta)
    return builder.done(use_texture=use_texture)


def add_jbm_font(size: int, mdi_delta=0, ngc_delta=-4, *, use_texture=False) -> Font:
    jbm = get_jbm_nl_nfm_r_font_path()
    mdi = get_mdi_font_path()
    ngc = get_ngc_font_path()
    basename = os.path.basename(jbm)
    builder = FontBuilder(basename, size)
    builder.add_ttf(jbm)
    builder.add_ttf(mdi, size=size + mdi_delta)
    builder.add_ttf(ngc, size=size + ngc_delta)
    return builder.done(use_texture=use_texture)
