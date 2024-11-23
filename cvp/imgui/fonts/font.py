# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import imgui

# noinspection PyProtectedMember
from imgui.core import _Font

from cvp.fonts.cached_ttf import CachedTTF
from cvp.fonts.codepoint import Codepoint
from cvp.gl.texture import Texture


@dataclass
class Font:
    font: _Font
    family: str
    size: int
    block_step: int
    details: List[CachedTTF] = field(default_factory=list)
    blocks: List[Tuple[int, int]] = field(default_factory=list)
    texture: Optional[Texture] = None
    codepoints: Dict[int, Codepoint] = field(default_factory=dict)

    def __str__(self):
        return f"{self.family} ({self.size}px)"

    def __enter__(self):
        imgui.push_font(self.font)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        imgui.pop_font()

    def find_font_detail(self, codepoint: int) -> CachedTTF:
        for detail in self.details:
            if detail.has_codepoint(codepoint):
                return detail
        raise ValueError(f"Not found codepoint: {codepoint}")

    def get_font_detail(self, codepoint: int) -> Optional[CachedTTF]:
        try:
            return self.find_font_detail(codepoint)
        except ValueError:
            return None

    def get_codepoint_detail(self, codepoint: int) -> Codepoint:
        cp_detail = self.codepoints.get(codepoint)
        if cp_detail is None:
            font_detail = self.get_font_detail(codepoint)
            ttf = font_detail.ttf if font_detail is not None else None
            cp_detail = Codepoint(codepoint, ttf)
            self.codepoints[codepoint] = cp_detail
        return cp_detail

    def close(self) -> None:
        if self.texture is not None:
            self.texture.close()
