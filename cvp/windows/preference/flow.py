# -*- coding: utf-8 -*-

import imgui

from cvp.config.sections.flow.arcs import Arcs
from cvp.config.sections.flow.axis import Axis
from cvp.config.sections.flow.grid import Grid
from cvp.config.sections.flow.logs import Logs
from cvp.context.context import Context
from cvp.flow.datas.stroke import Stroke
from cvp.imgui.checkbox import checkbox
from cvp.imgui.color_edit4 import color_edit4
from cvp.imgui.combo import combo
from cvp.imgui.input_float import input_float
from cvp.imgui.input_int import input_int
from cvp.imgui.input_text import input_text
from cvp.types.override import override
from cvp.windows.preference._base import PreferenceWidget


class FlowPreference(PreferenceWidget):
    def __init__(self, context: Context, label="Flow"):
        self._config = context.config.flow_aui
        self._label = label

    @property
    @override
    def label(self) -> str:
        return self._label

    @staticmethod
    def tree_grid(label: str, grid: Grid) -> None:
        if imgui.tree_node(label):
            try:
                if visible := checkbox("Visible", grid.visible):
                    grid.visible = visible.state
                if step := input_float("Step", grid.step, step=1.0):
                    grid.step = step.value
                if thickness := input_float("Thickness", grid.thickness, step=1.0):
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
                if thickness := input_float("Thickness", axis.thickness, step=1.0):
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
                if thickness := input_float("Thickness", stroke.thickness, step=1.0):
                    stroke.thickness = thickness.value
                if rounding := input_float("Rounding", stroke.rounding, step=1.0):
                    stroke.rounding = rounding.value
            finally:
                imgui.tree_pop()

    @staticmethod
    def tree_logs(label: str, logs: Logs) -> None:
        if not imgui.tree_node(label):
            return

        try:
            if check := checkbox("Autoscroll", logs.autoscroll):
                logs.autoscroll = check.state

            if level := combo("Level", logs.level_index, logs.level_names):
                logs.level_index = level.value

            if filter_text := input_text("Filter", logs.filter):
                logs.filter = filter_text.value

            if lines := input_int("Lines", logs.lines):
                logs.lines = lines.value

            if color := color_edit4("Critical", *logs.critical_color):
                logs.critical_color = color.color
            if color := color_edit4("Error", *logs.error_color):
                logs.error_color = color.color
            if color := color_edit4("Warning", *logs.warning_color):
                logs.warning_color = color.color
            if color := color_edit4("Info", *logs.info_color):
                logs.info_color = color.color
            if color := color_edit4("Debug", *logs.debug_color):
                logs.debug_color = color.color
        finally:
            imgui.tree_pop()

    @staticmethod
    def tree_arcs(label: str, arcs: Arcs) -> None:
        if imgui.tree_node(label):
            try:
                if hovering_tolerance := input_float(
                    "Hovering tolerance",
                    arcs.hovering_tolerance,
                    step=1.0,
                ):
                    arcs.hovering_tolerance = hovering_tolerance.value
            finally:
                imgui.tree_pop()

    @override
    def on_process(self) -> None:
        self.tree_logs("Logs", self._config.logs)
        self.tree_grid("Grid X", self._config.grid_x)
        self.tree_grid("Grid Y", self._config.grid_x)
        self.tree_axis("Axis X", self._config.axis_x)
        self.tree_axis("Axis Y", self._config.axis_y)
        self.tree_arcs("Arcs", self._config.arcs)
