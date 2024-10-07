# -*- coding: utf-8 -*-

import imgui

from cvp.config.sections.layout import LayoutSection
from cvp.context import Context
from cvp.gui.button_ex import button_ex
from cvp.gui.input_text_disabled import input_text_disabled
from cvp.types import override
from cvp.widgets.tab import TabItem
from cvp.widgets.window_mapper import WindowMapper


class LayoutInfoTab(TabItem[LayoutSection]):
    def __init__(self, context: Context, windows: WindowMapper):
        super().__init__(context, "Info")
        self._windows = windows

    def has_layout(self, layout: LayoutSection) -> bool:
        return self.context.home.layouts.has_layout(str(layout.section))

    def save_layout(self, layout: LayoutSection) -> None:
        self.context.home.layouts.save_layout(str(layout.section))

    def load_layout(self, layout: LayoutSection) -> None:
        self.context.home.layouts.load_layout(str(layout.section))

    def remove_layout(self, layout: LayoutSection) -> None:
        self.context.home.layouts.remove_layout(str(layout.section))

    @override
    def on_item(self, item: LayoutSection) -> None:
        imgui.text("Section:")
        input_text_disabled("## Section", item.section)

        imgui.separator()

        if button_ex("Save"):
            self.save_layout(item)

        imgui.same_line()

        if button_ex("Load", disabled=not self.has_layout(item)):
            self.load_layout(item)

        imgui.same_line()

        if button_ex("Remove", disabled=not self.has_layout(item)):
            self.remove_layout(item)
