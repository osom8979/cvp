# -*- coding: utf-8 -*-

import imgui

from cvp.context.context import Context
from cvp.flow.datas.graph import Graph
from cvp.types.override import override
from cvp.widgets.tab import TabItem


class HistoryTab(TabItem[Graph]):
    def __init__(self, context: Context):
        super().__init__(context, "History")

    @override
    def on_item(self, item: Graph) -> None:
        imgui.bullet_text("History 1")
        imgui.bullet_text("History 2")
        imgui.bullet_text("History 3")
