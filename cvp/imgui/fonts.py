# -*- coding: utf-8 -*-

import os
from typing import List

import imgui
from cvp.assets import get_jbm_nl_nfm_r_font_path, get_mdi_font_path, get_ngc_font_path
from cvp.variables import FONT_RANGES_EXTENSION


def read_font_ranges(path: str) -> List[int]:
    result = list()
    with open(path, "rt") as file:
        for line in file:
            hex_values = line.strip().split()
            for hex_value in hex_values:
                result.append(int(hex_value.strip(), 16))
    return result


def create_glyph_ranges(path: str):
    ranges = read_font_ranges(path)
    ranges.append(0)
    return imgui.core.GlyphRanges(ranges)


def add_ngc_font(size_pixels: int, ranges_ext=FONT_RANGES_EXTENSION) -> None:
    mdi = get_mdi_font_path()
    ngc = get_ngc_font_path()

    mdi_ranges = create_glyph_ranges(os.path.splitext(mdi)[0] + ranges_ext)
    ngc_ranges = create_glyph_ranges(os.path.splitext(ngc)[0] + ranges_ext)

    io = imgui.get_io()
    merge_mode = imgui.core.FontConfig(merge_mode=True)

    io.fonts.add_font_from_file_ttf(ngc, size_pixels, None, ngc_ranges)
    io.fonts.add_font_from_file_ttf(mdi, size_pixels, merge_mode, mdi_ranges)


def add_jbm_font(size_pixels: int, ranges_ext=FONT_RANGES_EXTENSION) -> None:
    jbm = get_jbm_nl_nfm_r_font_path()
    mdi = get_mdi_font_path()
    ngc = get_ngc_font_path()

    jbm_ranges = create_glyph_ranges(os.path.splitext(jbm)[0] + ranges_ext)
    mdi_ranges = create_glyph_ranges(os.path.splitext(mdi)[0] + ranges_ext)

    io = imgui.get_io()
    merge_mode = imgui.core.FontConfig(merge_mode=True)
    korean_ranges = io.fonts.get_glyph_ranges_korean()

    io.fonts.add_font_from_file_ttf(jbm, size_pixels, None, jbm_ranges)
    io.fonts.add_font_from_file_ttf(mdi, size_pixels, merge_mode, mdi_ranges)
    io.fonts.add_font_from_file_ttf(ngc, size_pixels - 4, merge_mode, korean_ranges)
