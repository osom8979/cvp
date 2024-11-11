# -*- coding: utf-8 -*-

from typing import Final

import imgui

from cvp.context.context import Context
from cvp.flow.datas import Axis, Grid
from cvp.imgui.color_edit4 import color_edit4
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
                changed, state = imgui.checkbox("Visible", grid.visible)
                assert isinstance(changed, bool)
                assert isinstance(state, bool)
                if changed:
                    grid.visible = state

                changed, value = imgui.input_float("Step", grid.step)
                assert isinstance(changed, bool)
                assert isinstance(value, float)
                if changed:
                    grid.step = value

                changed, value = imgui.input_float("Thickness", grid.thickness)
                assert isinstance(changed, bool)
                assert isinstance(value, float)
                if changed:
                    grid.step = value

                if color_result := color_edit4("Color", *grid.color):
                    grid.color = color_result.color
            finally:
                imgui.tree_pop()

    @staticmethod
    def tree_axis(label: str, axis: Axis) -> None:
        if imgui.tree_node(label):
            try:
                changed, state = imgui.checkbox("Visible", axis.visible)
                assert isinstance(changed, bool)
                assert isinstance(state, bool)
                if changed:
                    axis.visible = state

                changed, value = imgui.input_float("Thickness", axis.thickness)
                assert isinstance(changed, bool)
                assert isinstance(value, float)
                if changed:
                    axis.step = value

                if color_result := color_edit4("Color", *axis.color):
                    axis.color = color_result.color
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

    def on_item_cursor(self, item: str) -> None:
        graph = self.context.fm.current_graph
        assert graph is not None

        input_text_disabled("Type", "-")
        input_text_disabled("Key", item)
