# -*- coding: utf-8 -*-

import os
import unicodedata
from math import isqrt
from typing import Mapping

import imgui

from cvp.config.sections.font import FontManagerConfig
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child
from cvp.imgui.draw_list import get_window_draw_list
from cvp.imgui.font import Font
from cvp.imgui.font_manager import FontMapper
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.item_width import item_width
from cvp.imgui.slider_float import slider_float
from cvp.types.override import override
from cvp.variables import (
    DEFAULT_API_SELECT_WIDTH,
    MAX_API_SELECT_WIDTH,
    MIN_API_SELECT_WIDTH,
)
from cvp.widgets.manager import Manager


class FontManager(Manager[FontManagerConfig, Font]):
    def __init__(self, context: Context, fonts: FontMapper):
        super().__init__(
            context=context,
            window_config=context.config.font_manager,
            title="Font",
            closable=True,
            flags=None,
        )
        self._fonts = fonts
        self._range_select_width = DEFAULT_API_SELECT_WIDTH
        self._min_range_select_width = MIN_API_SELECT_WIDTH
        self._max_range_select_width = MAX_API_SELECT_WIDTH
        self._plane_step = 0xFF
        self._selected_block = 0, 0
        self._text_color = 1.0, 1.0, 1.0, 1.0
        self._stroke_color = 1.0, 1.0, 1.0, 0.3
        self._rounding = 0.0
        self._rect_flags = 0
        self._thickness = 1.0
        self._padding = 4.0

    @override
    def get_menus(self) -> Mapping[str, Font]:
        return {key: value for key, value in self._fonts.items()}

    @override
    def on_process_sidebar_top(self) -> None:
        pass

    @override
    def on_menu(self, key: str, item: Font) -> None:
        imgui.text("Font information")
        imgui.separator()

        input_text_disabled("Font family", item.family)
        input_text_disabled("Font pixel size", str(item.size))

        with begin_child("Planes", width=self._range_select_width):
            with item_width(-1):
                self.slider_range_select_width()
                list_box = imgui.begin_list_box("##Planes", width=-1, height=-1)
                if list_box.opened:
                    with list_box:
                        self.selectable_blocks(item)

        imgui.same_line()

        with begin_child("Codepoints", width=-1, height=-1, border=True):
            self.draw_codepoint_matrix(item)

    def slider_range_select_width(self) -> None:
        result = slider_float(
            "## Unicode Range List Width",
            self._range_select_width,
            self._min_range_select_width,
            self._max_range_select_width,
            "List width (%.3f)",
        )
        if result:
            self._range_select_width = result.value

    def selectable_blocks(self, item: Font) -> None:
        for block in item.blocks:
            begin, end = block
            label = f"{begin:06X}-{end:06X}"
            if imgui.selectable(label, block == self._selected_block)[1]:
                self._selected_block = block

    def draw_codepoint_matrix(self, item: Font) -> None:
        codepoint_begin = self._selected_block[0]
        stroke_color = imgui.get_color_u32_rgba(*self._stroke_color)
        text_color = imgui.get_color_u32_rgba(*self._text_color)
        padding = self._padding
        rounding = self._rounding
        rect_flags = self._rect_flags
        thickness = self._thickness

        cx, cy = imgui.get_cursor_screen_pos()
        draw_list = get_window_draw_list()
        cell_size = item.size
        block_step = item.block_step
        line_count = isqrt(block_step)

        for i in range(block_step):
            x = i % line_count
            y = i // line_count

            x1 = cx + x * (cell_size + padding)
            y1 = cy + y * (cell_size + padding)
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            roi = x1, y1, x2, y2
            draw_list.add_rect(*roi, stroke_color, rounding, rect_flags, thickness)

            codepoint = codepoint_begin + i
            character = chr(codepoint)

            with item:
                draw_list.add_text(x1, y1, text_color, character)

            if imgui.is_mouse_hovering_rect(*roi):
                with imgui.begin_tooltip():
                    try:
                        name = unicodedata.name(character)
                    except ValueError:
                        name = "[Unknown]"

                    try:
                        detail = item.find_detail(codepoint)
                        filename = os.path.basename(detail.ttf.path)
                        glyph = detail.ttf.ttf.getBestCmap().get(codepoint)
                    except KeyError:
                        filename = "[Unknown]"
                        glyph = "[Unknown]"

                    category = unicodedata.category(character)
                    combining = unicodedata.combining(character)
                    bidirectional = unicodedata.bidirectional(character)

                    message = (
                        f"{character}\n"
                        f"Codepoint: U+{codepoint:06X}\n"
                        f"Name: {name}\n"
                        f"Category: {category}\n"
                        f"Combining: {combining}\n"
                        f"Bidirectional: {bidirectional}\n"
                        f"Glyph: {glyph}\n"
                        f"Filename: {filename}"
                    )
                    imgui.text_unformatted(message)
