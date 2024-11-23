# -*- coding: utf-8 -*-

import unicodedata
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import imgui

# noinspection PyProtectedMember
from imgui.core import _Font

from cvp.fonts.cached_ttf import CachedTTF
from cvp.fonts.ttf import TTF
from cvp.gl.texture import Texture


class CodepointDetail:
    def __init__(self, codepoint: int, ttf: Optional[TTF] = None):
        self.codepoint = codepoint
        self.character = chr(codepoint)
        self.category = str()
        self.combining = 0
        self.bidirectional = str()
        self.name = str()
        self.exists = False
        self.filepath = str()
        self.filename = str()
        self.glyph = str()

        try:
            self.category = unicodedata.category(self.character)
            self.combining = unicodedata.combining(self.character)
            self.bidirectional = unicodedata.bidirectional(self.character)
            self.name = unicodedata.name(self.character)
        except ValueError:
            pass

        if ttf is not None:
            self.exists = True
            self.filepath = str(ttf.path)
            self.filename = ttf.basename
            self.glyph = ttf.get_best_camp().get(codepoint, str())

    def __bool__(self):
        return self.exists

    def as_printable_unicode(self) -> str:
        return f"\\U{self.codepoint:08X}"

    def as_unformatted_text(self):
        return (
            f"{self.character}\n"
            f"Codepoint: U+{self.codepoint:06X}\n"
            f"Name: {self.name}\n"
            f"Category: {self.category}\n"
            f"Combining: {self.combining}\n"
            f"Bidirectional: {self.bidirectional}\n"
            f"Glyph: {self.glyph}\n"
            f"Filename: {self.filename}\n"
        )


@dataclass
class Font:
    font: _Font
    family: str
    size: int
    block_step: int
    details: List[CachedTTF] = field(default_factory=list)
    blocks: List[Tuple[int, int]] = field(default_factory=list)
    texture: Optional[Texture] = None
    codepoints: Dict[int, CodepointDetail] = field(default_factory=dict)

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

    def get_codepoint_detail(self, codepoint: int) -> CodepointDetail:
        cp_detail = self.codepoints.get(codepoint)
        if cp_detail is None:
            font_detail = self.get_font_detail(codepoint)
            ttf = font_detail.ttf if font_detail is not None else None
            cp_detail = CodepointDetail(codepoint, ttf)
            self.codepoints[codepoint] = cp_detail
        return cp_detail

    def close(self) -> None:
        if self.texture is not None:
            self.texture.close()
