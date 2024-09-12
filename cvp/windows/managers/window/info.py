# -*- coding: utf-8 -*-

import imgui

from cvp.context import Context
from cvp.types import override
from cvp.widgets import input_text_disabled
from cvp.widgets.hoc.tab import TabItem
from cvp.widgets.hoc.window import Window


class WindowInfoTab(TabItem[Window]):
    def __init__(self, context: Context):
        super().__init__(context, "Info")

    @override
    def on_item(self, item: Window) -> None:
        imgui.text("Key:")
        input_text_disabled("## Label", item.key)

        imgui.text("Title:")
        input_text_disabled("## Title", item.title)

        imgui.text("Label:")
        input_text_disabled("## Label", item.label)
