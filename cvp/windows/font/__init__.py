# -*- coding: utf-8 -*-

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
from cvp.strings.unicode.planes import PLANES
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
        self._selected_range = 0, 0
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

    def selectable_planes(self) -> None:
        for plane in PLANES:
            if plane.unassigned:
                continue

            name = plane.short_name
            for plane_range in plane.split_ranges(self._plane_step):
                begin, end = plane_range
                label = f"{name} [U+{begin:04X}, U+{end:04X}]"
                if imgui.selectable(label, plane_range == self._selected_range)[1]:
                    self._selected_range = plane_range

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
                        self.selectable_planes()

        imgui.same_line()

        with begin_child("Codepoints", width=-1, height=-1, border=True):
            cx, cy = imgui.get_cursor_screen_pos()
            draw_list = get_window_draw_list()
            with item:
                cell_size = item.size
                line_count = isqrt(self._plane_step)
                codepoint_begin = self._selected_range[0]
                for i in range(self._plane_step):
                    x = i % line_count
                    y = i // line_count

                    x1 = cx + x * (cell_size + self._padding)
                    y1 = cy + y * (cell_size + self._padding)
                    x2 = x1 + cell_size
                    y2 = y1 + cell_size

                    roi = x1, y1, x2, y2
                    draw_list.add_rect(
                        *roi,
                        imgui.get_color_u32_rgba(*self._stroke_color),
                        self._rounding,
                        self._rect_flags,
                        self._thickness,
                    )

                    codepoint = codepoint_begin + i
                    char = chr(codepoint)
                    draw_list.add_text(
                        x1,
                        y1,
                        imgui.get_color_u32_rgba(*self._text_color),
                        char,
                    )

                    if imgui.is_mouse_hovering_rect(*roi):
                        with imgui.begin_tooltip():
                            try:
                                name = unicodedata.name(char)
                            except ValueError:
                                name = "[Unknown]"

                            category = unicodedata.category(char)
                            combining = unicodedata.combining(char)
                            bidirectional = unicodedata.bidirectional(char)

                            message = (
                                f"U+{codepoint:06X}\n"
                                f"{char}\n"
                                f"Name: {name}\n"
                                f"Category: {category}\n"
                                f"Combining: {combining}\n"
                                f"Bidirectional: {bidirectional}"
                            )
                            imgui.text_unformatted(message)
