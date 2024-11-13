# -*- coding: utf-8 -*-

from typing import Mapping

import imgui

from cvp.config.sections.font import FontManagerConfig
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child
from cvp.imgui.font_manager import FontItem, FontMapper
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


class FontManager(Manager[FontManagerConfig, FontItem]):
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

    @override
    def get_menus(self) -> Mapping[str, FontItem]:
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

    @override
    def on_menu(self, key: str, item: FontItem) -> None:
        imgui.text("Font information")
        imgui.separator()

        input_text_disabled("Font family", item.family)
        input_text_disabled("Font pixel size", str(item.size_pixels))

        with begin_child("Unicode Range List", width=self._range_select_width):
            with item_width(-1):
                self.slider_range_select_width()

                # list_box = imgui.begin_list_box(
                #     "## Unicode Range List Box",
                #     width=-1,
                #     height=-1,
                # )
                # if list_box.opened:
                #     with list_box:
                #         for key in apis.keys():
                #             if imgui.selectable(key, key == item.select_api)[1]:
                #                 item.select_api = key

        # import unicodedata
        # for codepoint in range(0x110000):
        #     char = chr(codepoint)
        #     try:
        #         name = unicodedata.name(char)
        #     except ValueError:
        #         name = "No name"
        #
        #     category = unicodedata.category(char)
        #     combining = unicodedata.combining(char)
        #     bidirectional = unicodedata.bidirectional(char)
        #
        #     print(f"U+{codepoint:04X} {char} - Name: {name}, Category: {category}, "
        #           f"Combining: {combining}, Bidirectional: {bidirectional}")
