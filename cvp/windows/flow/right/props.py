# -*- coding: utf-8 -*-

from typing import Final

import imgui

from cvp.context.context import Context
from cvp.flow.datas import Axis, Grid, Stroke, Style
from cvp.imgui.checkbox import checkbox
from cvp.imgui.color_edit4 import color_edit4
from cvp.imgui.input_float import input_float
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.input_text_value import input_text_value
from cvp.types.override import override
from cvp.widgets.tab import TabItem

INPUT_BUFFER: Final[int] = 256
ENTER_RETURN: Final[int] = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE


class PropsTab(TabItem[str]):
    def __init__(self, context: Context):
        super().__init__(context, "Props")

    @override
    def on_item(self, item: str) -> None:
        if self.context.fm.opened:
            if item:
                self.on_item_cursor(item)
            else:
                self.on_graph_cursor()
        else:
            self.on_none()

    @override
    def on_none(self) -> None:
        pass

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

    def on_graph_cursor(self) -> None:
        graph = self.context.fm.current_graph
        assert graph is not None

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

    def on_item_cursor(self, item: str) -> None:
        graph = self.context.fm.current_graph
        assert graph is not None

        input_text_disabled("Type", "Node")
        input_text_disabled("Key", item)
