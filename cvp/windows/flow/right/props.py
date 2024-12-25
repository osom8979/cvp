# -*- coding: utf-8 -*-

from typing import Final, List

import imgui

from cvp.context.context import Context
from cvp.flow.datas import Arc, Axis, Grid, Node, Stroke, Style
from cvp.flow.datas.graph import Graph
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
        nodes = item.find_selected_nodes()
        arcs = item.find_selected_arcs()
        count = len(nodes) + len(arcs)
        assert 0 <= count
        if count == 0:
            self.on_graph_cursor(item)
        elif count == 1:
            if nodes:
                assert 1 == len(nodes)
                assert 0 == len(arcs)
                self.on_node_cursor(nodes[0])
            else:
                assert 0 == len(nodes)
                assert 1 == len(arcs)
                self.on_arc_cursor(arcs[0])
        else:
            self.on_multiple_cursor(nodes, arcs)

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

    def on_arc_cursor(self, arc: Arc) -> None:
        input_text_disabled("Type", type(arc).__name__)
        input_text_disabled("UUID", arc.uuid)

        arc.name = input_text_value("Name", arc.name)
        arc.docs = input_text_value("Docs", arc.docs)

        # arc.output
        # arc.input

    def on_multiple_cursor(self, nodes: List[Node], arcs: List[Arc]) -> None:
        input_text_disabled("Type", "Multiple")
