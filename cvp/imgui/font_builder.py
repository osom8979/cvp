# -*- coding: utf-8 -*-

from os import PathLike
from typing import List, Optional, Tuple, Union

import imgui

# noinspection PyProtectedMember
from imgui.core import FontConfig, GlyphRanges, _Font

from cvp.fonts.ranges import UNICODE_SINGLE_BLOCK_SIZE, CodepointRange, flatten_ranges
from cvp.fonts.ttf import TTF
from cvp.gl.texture import Texture
from cvp.imgui.font import Font, FontDetail


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
    _details: List[FontDetail]

    def __init__(self, name: str, size: int):
        self._font = None
        self._name = name
        self._size = size
        self._merge = FontConfig(merge_mode=True)
        self._details = list()

    @property
    def name(self):
        return self._name

    @property
    def size(self):
        return self._size

    @property
    def fonts(self):
        return imgui.get_io().fonts

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
        self._details.append(FontDetail(ttf, ranges, size))
        return self

    @staticmethod
    def _create_font_texture() -> Texture:
        texture = Texture()
        width, height, pixels = imgui.get_io().fonts.get_tex_data_as_alpha8()
        texture.open(width, height)
        with texture:
            texture.update_alpha_texture(pixels)
        return texture

    def _create_blocks(self, step=UNICODE_SINGLE_BLOCK_SIZE) -> List[Tuple[int, int]]:
        result = set()
        for detail in self._details:
            for cp_range in detail.ranges:
                for block_range in cp_range.as_blocks(step):
                    result.add(block_range)
        return list(sorted(result, key=lambda x: x[0]))

    def done(self, block_step=UNICODE_SINGLE_BLOCK_SIZE, *, use_texture=False) -> Font:
        return Font(
            self._font,
            self._name,
            self._size,
            block_step,
            self._details,
            self._create_blocks(block_step),
            self._create_font_texture() if use_texture else None,
        )
