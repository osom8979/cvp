# -*- coding: utf-8 -*-

import imgui

from cvp.context.context import Context
from cvp.flow.datas.graph import Graph
from cvp.imgui.fonts.mapper import FontMapper
from cvp.imgui.text_centered import text_centered
from cvp.types.override import override
from cvp.widgets.tab import TabItem


class TreeTab(TabItem[Graph]):
    def __init__(self, context: Context, fonts: FontMapper):
        super().__init__(context, "Tree")
        self._fonts = fonts

    @override
    def on_item(self, item: Graph) -> None:
        if imgui.tree_node(item.name, imgui.TREE_NODE_DEFAULT_OPEN):
            flow_pin_n_icon = item.style.flow_pin_n_icon
            flow_pin_y_icon = item.style.flow_pin_y_icon
            data_pin_n_icon = item.style.data_pin_n_icon
            data_pin_y_icon = item.style.data_pin_y_icon

            for node in item.nodes:
                node_label = f"{node.name}##{node.uuid}"
                if imgui.tree_node(node_label):
                    for pin in node.flow_pins:
                        pin_icon = flow_pin_y_icon if pin.connected else flow_pin_n_icon
                        with self._fonts.normal_icon:
                            imgui.text(pin_icon)
                        imgui.same_line()
                        imgui.text(pin.name)

                    for pin in node.data_pins:
                        pin_icon = data_pin_y_icon if pin.connected else data_pin_n_icon
                        with self._fonts.normal_icon:
                            imgui.text(pin_icon)
                        imgui.same_line()
                        imgui.text(pin.name)
                    imgui.tree_pop()
            imgui.tree_pop()

    @override
    def on_none(self) -> None:
        text_centered("Please select a graph")
