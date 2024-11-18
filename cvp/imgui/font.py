# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List, NamedTuple, Optional

import imgui

# noinspection PyProtectedMember
from imgui.core import _Font

from cvp.fonts.ranges import CodepointRange
from cvp.fonts.ttf import TTF
from cvp.gl.texture import Texture


class TTFItem(NamedTuple):
    ttf: TTF
    ranges: List[CodepointRange]
    size: int

    def has_codepoint(self, codepoint: int) -> bool:
        for begin, end in self.ranges:
            if begin <= codepoint <= end:
                return True
        return False


@dataclass
class Font:
    font: _Font
    family: str
    size: int
    ttfs: List[TTFItem] = field(default_factory=list)
    texture: Optional[Texture] = None

    def __str__(self):
        return f"{self.family} ({self.size}px)"

    def __enter__(self):
        imgui.push_font(self.font)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        imgui.pop_font()

    def close(self) -> None:
        if self.texture is not None:
            self.texture.close()
