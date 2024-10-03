# -*- coding: utf-8 -*-

import imgui

from cvp.context import Context
from cvp.flow.graph import FlowGraph
from cvp.types import override
from cvp.widgets.tab import TabItem


class TreeTab(TabItem[FlowGraph]):
    def __init__(self, context: Context):
        super().__init__(context, "Tree")

    @override
    def on_item(self, item: FlowGraph) -> None:
        if imgui.tree_node(item.class_name, imgui.TREE_NODE_DEFAULT_OPEN):
            imgui.tree_pop()
