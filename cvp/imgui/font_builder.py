# -*- coding: utf-8 -*-

from os import PathLike
from typing import List, Optional, Union

import imgui

# noinspection PyProtectedMember
from imgui.core import FontConfig, GlyphRanges, _Font

from cvp.fonts.ranges import CodepointRange, flatten_ranges
from cvp.fonts.ttf import TTF
from cvp.gl.texture import Texture
from cvp.imgui.font import Font, TTFItem


def create_glyph_ranges(ranges: List[CodepointRange]) -> GlyphRanges:
    if ranges:
        # [IMPORTANT]
        # The NULL character is a special character used as a termination character
        # and should not be used.
        if ranges[0].begin == 0:
            if ranges[0].end == 0:
                # If the range is 0x00 to 0x00, remove the element.
                ranges = ranges[1:]
            else:
                assert ranges[0].begin + 1 <= ranges[0].end
                first_element = CodepointRange(ranges[0].begin + 1, ranges[0].end)
                ranges = [first_element] + ranges[1:]

    glyph_ranges = flatten_ranges(ranges)
    assert len(glyph_ranges) % 2 == 0

    # GlyphRanges must be terminated with a NULL (0) element.
    glyph_ranges.append(0)

    return GlyphRanges(glyph_ranges)


class FontBuilder:
    _font: Optional[_Font]
    _ttfs: List[TTFItem]

    def __init__(self, name: str, size: int):
        self._font = None
        self._name = name
        self._size = size
        self._merge = FontConfig(merge_mode=True)
        self._ttfs = list()

    @property
    def name(self):
        return self._name

    @property
    def size(self):
        return self._size

    def add_ttf(
        self,
        path: Union[str, PathLike[str]],
        ranges: Optional[List[CodepointRange]] = None,
        *,
        size: Optional[int] = None,
    ):
        ttf = TTF(path)

        if not ranges:
            ranges = ttf.get_glyph_ranges()

        if not size:
            size = self._size

        if not ranges:
            raise ValueError("Invalid ranges")
        if not size:
            raise ValueError("Invalid size")
        if size < 0:
            raise ValueError("Invalid size")

        self._font = imgui.get_io().fonts.add_font_from_file_ttf(
            str(ttf.path),
            size,
            None if self._font is None else self._merge,
            create_glyph_ranges(ranges),
        )
        self._ttfs.append(TTFItem(ttf, ranges, size))
        return self

    def done(self, *, use_texture=False) -> Font:
        if use_texture:
            texture = Texture()
            width, height, pixels = imgui.get_io().fonts.get_tex_data_as_alpha8()
            texture.open(width, height)
            with texture:
                texture.update_alpha_texture(pixels)
        else:
            texture = None
        return Font(self._font, self._name, self._size, self._ttfs, texture)
