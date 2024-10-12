# -*- coding: utf-8 -*-

import imgui

from cvp.context.context import Context
from cvp.flow.datas import Graph
from cvp.types import override
from cvp.widgets.tab import TabItem


class TreeTab(TabItem[Graph]):
    def __init__(self, context: Context):
        super().__init__(context, "Tree")

    @override
    def on_item(self, item: Graph) -> None:
        if imgui.tree_node(item.name, imgui.TREE_NODE_DEFAULT_OPEN):
            for node in item.nodes:
                if imgui.tree_node(node.name, imgui.TREE_NODE_DEFAULT_OPEN):
                    for pin in node.pins:
                        imgui.text(pin.name)
                    imgui.tree_pop()
            imgui.tree_pop()
