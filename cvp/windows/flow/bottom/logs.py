# -*- coding: utf-8 -*-

import imgui

from cvp.context.context import Context
from cvp.flow.datas.graph import Graph
from cvp.imgui.begin_child import begin_child
from cvp.imgui.fonts.mapper import FontMapper
from cvp.types.override import override
from cvp.widgets.tab import TabItem
from cvp.windows.flow.cursor import FlowCursor


class LogsTab(TabItem[Graph]):
    def __init__(self, context: Context, fonts: FontMapper, cursor: FlowCursor):
        super().__init__(context, "Logs")
        self._fonts = fonts
        self._cursor = cursor
        self._auto_scroll = False

    @override
    def on_process(self) -> None:
        with begin_child("## Logging", border=False):
            imgui.text_unformatted("Empty logging")

            if self._auto_scroll:
                imgui.set_scroll_here_y(1.0)
