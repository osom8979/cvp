# -*- coding: utf-8 -*-

import imgui
from cvp.context import Context
from cvp.flow.instances.graph import Graph
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.text_centered import text_centered
from cvp.types import override
from cvp.widgets.tab import TabItem


class GraphTab(TabItem[Graph]):
    def __init__(self, context: Context):
        super().__init__(context, "Graph")

    @override
    def on_item(self, item: Graph) -> None:
        if item is None:
            text_centered("Please select a graph")
            return

        imgui.text("Name:")
        input_text_disabled("## Name", item.name)
