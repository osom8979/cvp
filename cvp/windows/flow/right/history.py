# -*- coding: utf-8 -*-

import imgui

from cvp.context.context import Context
from cvp.flow.datas.graph import Graph
from cvp.imgui.fonts.mapper import FontMapper
from cvp.types.override import override
from cvp.widgets.tab import TabItem
from cvp.windows.flow.cursor import FlowCursor


class HistoryTab(TabItem[Graph]):
    def __init__(self, context: Context, fonts: FontMapper, cursor: FlowCursor):
        super().__init__(context, "History")
        self._fonts = fonts
        self._cursor = cursor

    @override
    def on_item(self, item: Graph) -> None:
        imgui.bullet_text("History 1")
        imgui.bullet_text("History 2")
        imgui.bullet_text("History 3")
