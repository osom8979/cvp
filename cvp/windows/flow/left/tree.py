# -*- coding: utf-8 -*-

import imgui

from cvp.context.context import Context
from cvp.flow.datas.graph import Graph
from cvp.flow.datas.node import Node
from cvp.imgui.fonts.mapper import FontMapper
from cvp.imgui.text_centered import text_centered
from cvp.types.override import override
from cvp.widgets.tab import TabItem
from cvp.windows.flow.cursor import FlowCursor

_LEAF = imgui.TREE_NODE_LEAF
_NO_TREE_PUSH_ON_OPEN = imgui.TREE_NODE_NO_TREE_PUSH_ON_OPEN
_OPEN_ON_ARROW = imgui.TREE_NODE_OPEN_ON_ARROW
_OPEN_ON_DOUBLE_CLICK = imgui.TREE_NODE_OPEN_ON_DOUBLE_CLICK
_SPAN_AVAILABLE_WIDTH = imgui.TREE_NODE_SPAN_AVAILABLE_WIDTH

NODE_FLAGS = _OPEN_ON_ARROW | _OPEN_ON_DOUBLE_CLICK | _SPAN_AVAILABLE_WIDTH
PIN_FLAGS = NODE_FLAGS | _LEAF | _NO_TREE_PUSH_ON_OPEN
ARC_FLAGS = NODE_FLAGS | _LEAF | _NO_TREE_PUSH_ON_OPEN


class TreeTab(TabItem[Graph]):
    def __init__(self, context: Context, fonts: FontMapper, cursor: FlowCursor):
        super().__init__(context, "Tree")
        self._fonts = fonts
        self._cursor = cursor

    @override
    def on_none(self) -> None:
        text_centered("Please select a graph")

    @override
    def on_item(self, item: Graph) -> None:
        if imgui.tree_node(item.name, imgui.TREE_NODE_DEFAULT_OPEN):
            try:
                for node in item.nodes:
                    self.on_node(item, node)
            finally:
                imgui.tree_pop()

    def on_node(self, graph: Graph, node: Node) -> None:
        flow_pin_n_icon = self.context.config.flow_aui.pins.flow_n_icon
        flow_pin_y_icon = self.context.config.flow_aui.pins.flow_y_icon
        data_pin_n_icon = self.context.config.flow_aui.pins.data_n_icon
        data_pin_y_icon = self.context.config.flow_aui.pins.data_y_icon
        key_ctrl = imgui.get_io().key_ctrl

        flags = NODE_FLAGS
        if node.selected:
            flags |= imgui.TREE_NODE_SELECTED

        node_opened = imgui.tree_node(f"{node.name}##{node.uuid}", flags)
        if imgui.is_item_clicked() and not imgui.is_item_toggled_open():
            if not key_ctrl:
                graph.unselect_all_items()
            graph.flip_select_item(node)

        if not node_opened:
            return

        try:
            for i, pin in enumerate(node.pins):
                if pin.is_flow_action:
                    pin_icon = flow_pin_y_icon if pin.connected else flow_pin_n_icon
                elif pin.is_data_action:
                    pin_icon = data_pin_y_icon if pin.connected else data_pin_n_icon
                else:
                    assert False, "Inaccessible section"

                flags = PIN_FLAGS
                if pin.selected:
                    flags |= imgui.TREE_NODE_SELECTED

                imgui.tree_node(f"{pin.name}##{i}", flags)
                if imgui.is_item_clicked() and not imgui.is_item_toggled_open():
                    if not key_ctrl:
                        graph.unselect_all_items()
                    graph.flip_select_item(pin)

                imgui.same_line(imgui.get_cursor_pos_x())

                with self._fonts.normal_icon:
                    imgui.text(pin_icon)
        finally:
            imgui.tree_pop()
