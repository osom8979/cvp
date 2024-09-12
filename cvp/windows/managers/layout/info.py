# -*- coding: utf-8 -*-

import imgui

from cvp.config.sections.windows.layout import LayoutSection
from cvp.context import Context
from cvp.types import override
from cvp.widgets import input_text_disabled, input_text_value, item_width
from cvp.widgets.hoc.tab import TabItem
from cvp.widgets.hoc.window_mapper import WindowMapper


class LayoutInfoTab(TabItem[LayoutSection]):
    def __init__(self, context: Context, windows: WindowMapper):
        super().__init__(context, "Info")
        self._windows = windows

    @override
    def on_item(self, item: LayoutSection) -> None:
        imgui.text("Section:")
        input_text_disabled("## Section", item.section)

        imgui.text("Title:")
        with item_width(-1):
            item.title = input_text_value("## Title", item.title)
