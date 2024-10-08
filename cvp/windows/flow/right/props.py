# -*- coding: utf-8 -*-

import imgui
from cvp.context.context import Context
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.types import override
from cvp.widgets.tab import TabItem


class PropsTab(TabItem[str]):
    def __init__(self, context: Context):
        super().__init__(context, "Props")

    @override
    def on_item(self, item: str) -> None:
        imgui.text("Key:")
        input_text_disabled("## Key", item)
