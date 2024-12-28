# -*- coding: utf-8 -*-

from typing import Final

import imgui

from cvp.context.context import Context
from cvp.flow.datas.arc import Arc
from cvp.flow.datas.axis import Axis
from cvp.flow.datas.graph import Graph
from cvp.flow.datas.grid import Grid
from cvp.flow.datas.node import Node
from cvp.flow.datas.pin import Pin
from cvp.flow.datas.selected_items import SelectedItems
from cvp.flow.datas.stroke import Stroke
from cvp.flow.datas.style import Style
from cvp.imgui.checkbox import checkbox
from cvp.imgui.color_edit4 import color_edit4
from cvp.imgui.input_float import input_float
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.input_text_value import input_text_value
from cvp.types.override import override
from cvp.widgets.tab import TabItem

INPUT_BUFFER: Final[int] = 256
ENTER_RETURN: Final[int] = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE


class PropsTab(TabItem[Graph]):
    def __init__(self, context: Context):
        super().__init__(context, "Props")

    @override
    def on_item(self, item: Graph) -> None:
        items = item.find_selected_items()
        if len(items) == 0:
            self.on_graph_cursor(item)
        elif len(items) == 1:
            if items.nodes:
                assert 1 == len(items.nodes)
                assert 0 == len(items.pins)
                assert 0 == len(items.arcs)
                self.on_node_cursor(items.nodes[0])
            elif items.pins:
                assert 0 == len(items.nodes)
                assert 1 == len(items.pins)
                assert 0 == len(items.arcs)
                self.on_pin_cursor(items.pins[0])
            elif items.arcs:
                assert 0 == len(items.nodes)
                assert 0 == len(items.pins)
                assert 1 == len(items.arcs)
                self.on_arc_cursor(items.arcs[0])
            else:
                assert False, "Inaccessible section"
        else:
            assert 2 <= len(items)
            self.on_multiple_cursor(items)

    @staticmethod
    def tree_grid(label: str, grid: Grid) -> None:
        if imgui.tree_node(label):
            try:
                if visible := checkbox("Visible", grid.visible):
                    grid.visible = visible.state
                if step := input_float("Step", grid.step):
                    grid.step = step.value
                if thickness := input_float("Thickness", grid.thickness):
                    grid.thickness = thickness.value
                if color := color_edit4("Color", *grid.color):
                    grid.color = color.color
            finally:
                imgui.tree_pop()

    @staticmethod
    def tree_axis(label: str, axis: Axis) -> None:
        if imgui.tree_node(label):
            try:
                if visible := checkbox("Visible", axis.visible):
                    axis.visible = visible
                if thickness := input_float("Thickness", axis.thickness):
                    axis.thickness = thickness.value
                if color := color_edit4("Color", *axis.color):
                    axis.color = color.color
            finally:
                imgui.tree_pop()

    @staticmethod
    def tree_stroke(label: str, stroke: Stroke) -> None:
        if imgui.tree_node(label):
            try:
                if color := color_edit4("Color", *stroke.color):
                    stroke.color = color.color
                if thickness := input_float("Thickness", stroke.thickness):
                    stroke.thickness = thickness.value
                if rounding := input_float("Rounding", stroke.rounding):
                    stroke.rounding = rounding.value
            finally:
                imgui.tree_pop()

    @staticmethod
    def tree_style_colors(label: str, style: Style) -> None:
        if imgui.tree_node(label):
            try:
                if color := color_edit4("Normal", *style.normal_color):
                    style.normal_color = color.color
                if color := color_edit4("Hovering", *style.hovering_color):
                    style.hovering_color = color.color
                if color := color_edit4("Layout", *style.layout_color):
                    style.layout_color = color.color
            finally:
                imgui.tree_pop()

    def on_graph_cursor(self, graph: Graph) -> None:
        input_text_disabled("Type", "Graph")
        input_text_disabled("UUID", graph.uuid)

        graph.name = input_text_value("Name", graph.name)
        graph.docs = input_text_value("Docs", graph.docs)

        if color_result := color_edit4("Color", *graph.color):
            graph.color = color_result.color

        self.tree_grid("Grid X", graph.grid_x)
        self.tree_grid("Grid Y", graph.grid_y)
        self.tree_axis("Axis X", graph.axis_x)
        self.tree_axis("Axis Y", graph.axis_y)
        self.tree_stroke("Selected node", graph.style.selected_node)
        self.tree_stroke("Hovering node", graph.style.hovering_node)
        self.tree_stroke("Normal node", graph.style.normal_node)
        self.tree_style_colors("Colors", graph.style)

        if show_layout := checkbox("Show layout", graph.style.show_layout):
            graph.style.show_layout = show_layout.state

    def on_node_cursor(self, node: Node) -> None:
        input_text_disabled("Type", type(node).__name__)
        input_text_disabled("UUID", node.uuid)

        node.name = input_text_value("Name", node.name)
        node.docs = input_text_value("Docs", node.docs)
        node.emblem = input_text_value("Emblem", node.emblem)

        if color_result := color_edit4("Color", *node.color):
            node.color = color_result.color

        # emblem_pos: Point = EMPTY_POINT
        # emblem_size: Size = EMPTY_SIZE
        # name_pos: Point = EMPTY_POINT
        # name_size: Size = EMPTY_SIZE
        # node_pos: Point = EMPTY_POINT
        # node_size: Size = EMPTY_SIZE

        # flow_inputs: List[Pin] = field(default_factory=list)
        # flow_outputs: List[Pin] = field(default_factory=list)

        # data_inputs: List[Pin] = field(default_factory=list)
        # data_outputs: List[Pin] = field(default_factory=list)

    def on_pin_cursor(self, pin: Pin) -> None:
        input_text_disabled("Type", type(pin).__name__)
        input_text_disabled("Name", pin.name)

    def on_arc_cursor(self, arc: Arc) -> None:
        input_text_disabled("Type", type(arc).__name__)
        input_text_disabled("UUID", arc.uuid)

        arc.name = input_text_value("Name", arc.name)
        arc.docs = input_text_value("Docs", arc.docs)

        # arc.output
        # arc.input

    def on_multiple_cursor(self, items: SelectedItems) -> None:
        input_text_disabled("Type", "Multiple")
