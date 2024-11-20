# -*- coding: utf-8 -*-

import os
import unicodedata
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import imgui

# noinspection PyProtectedMember
from imgui.core import _Font

from cvp.fonts.ranges import CodepointRange
from cvp.fonts.ttf import TTF
from cvp.gl.texture import Texture


@dataclass
class FontDetail:
    ttf: TTF
    ranges: List[CodepointRange]
    size: int

    def has_codepoint(self, codepoint: int) -> bool:
        for begin, end in self.ranges:
            if begin <= codepoint <= end:
                return True
        return False

    @property
    def best_camp(self) -> Dict[int, str]:
        return self.ttf.ttf.getBestCmap()


class CodepointDetail:
    def __init__(self, codepoint: int, detail: Optional[FontDetail] = None):
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

        if detail is not None:
            self.exists = True
            self.filepath = str(detail.ttf.path)
            self.filename = os.path.basename(detail.ttf.path)
            self.glyph = detail.best_camp.get(codepoint, str())

    def __bool__(self):
        return self.exists

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
    details: List[FontDetail] = field(default_factory=list)
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

    def find_font_detail(self, codepoint: int) -> FontDetail:
        for detail in self.details:
            if detail.has_codepoint(codepoint):
                return detail
        raise ValueError(f"Not found codepoint: {codepoint}")

    def get_font_detail(self, codepoint: int) -> Optional[FontDetail]:
        try:
            return self.find_font_detail(codepoint)
        except ValueError:
            return None

    def get_codepoint_detail(self, codepoint: int) -> CodepointDetail:
        cp_detail = self.codepoints.get(codepoint)
        if cp_detail is None:
            font_detail = self.get_font_detail(codepoint)
            cp_detail = CodepointDetail(codepoint, font_detail)
            self.codepoints[codepoint] = cp_detail
        return cp_detail

    def close(self) -> None:
        if self.texture is not None:
            self.texture.close()
