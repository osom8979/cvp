# -*- coding: utf-8 -*-

import imgui

from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child
from cvp.types.override import override
from cvp.widgets.tab import TabItem


class LogsTab(TabItem[str]):
    def __init__(self, context: Context):
        super().__init__(context, "Logs")
        self._auto_scroll = False

    @override
    def on_item(self, item: str) -> None:
        with begin_child("## Logging", border=False):
            imgui.text_unformatted(item)

            if self._auto_scroll:
                imgui.set_scroll_here_y(1.0)
