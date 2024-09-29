# -*- coding: utf-8 -*-

import imgui

from cvp.context import Context
from cvp.flow.graph import FlowGraph
from cvp.gui.input_text_disabled import input_text_disabled
from cvp.gui.text_centered import text_centered
from cvp.types import override
from cvp.widgets.tab import TabItem


class GraphTab(TabItem[FlowGraph]):
    def __init__(self, context: Context):
        super().__init__(context, "Graph")

    @override
    def on_item(self, item: FlowGraph) -> None:
        if item is None:
            text_centered("Please select a graph")
            return

        imgui.text("Name:")
        input_text_disabled("## Name", item.name)
