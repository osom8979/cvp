# -*- coding: utf-8 -*-

from typing import Optional

import imgui

from cvp.flow.datas import Axis
from cvp.flow.datas import Canvas as CanvasProps
from cvp.flow.datas import Grid
from cvp.renderer.widget.interface import WidgetInterface
from cvp.types.colors import RGBA
from cvp.types.override import override
from cvp.widgets.canvas._base import BaseCanvas


class IntegratedCanvas(BaseCanvas, WidgetInterface):
    def __init__(self, canvas_props: Optional[CanvasProps] = None):
        super().__init__(canvas_props)

    @override
    def on_process(self) -> None:
        self.next_state()
        assert self._draw_list is not None
        self.do_button_control()
        # draw_list = self._draw_list
        # mx, my = self._mouse_pos
        # cx, cy = self._canvas_pos
        # cw, ch = self._canvas_size
        # hovering = self._hovering
        # left_button = self._left_button_clicked
        # middle_button = self._middle_button_clicked
        # right_button = self._right_button_clicked

    def fill(self, color: RGBA) -> None:
        filled_color = imgui.get_color_u32_rgba(*color)
        cx, cy = self._canvas_pos
        cw, ch = self._canvas_size
        self._draw_list.add_rect_filled(cx, cy, cx + cw, cy + cy, filled_color)

    def draw_grid_x(self, grid_x: Grid) -> None:
        if not grid_x.visible:
            return

        color = imgui.get_color_u32_rgba(*grid_x.color)
        step = grid_x.step
        thickness = grid_x.thickness
        pos = self._canvas_pos
        size = self._canvas_size
        lines = self.vertical_grid_lines(step, pos, size)

        for line in lines:
            x1, y1, x2, y2 = line
            self._draw_list.add_line(x1, y1, x2, y2, color, thickness)

    def draw_grid_y(self, grid_y: Grid) -> None:
        if not grid_y.visible:
            return

        color = imgui.get_color_u32_rgba(*grid_y.color)
        step = grid_y.step
        thickness = grid_y.thickness
        pos = self._canvas_pos
        size = self._canvas_size
        lines = self.horizontal_grid_lines(step, pos, size)

        for line in lines:
            x1, y1, x2, y2 = line
            self._draw_list.add_line(x1, y1, x2, y2, color, thickness)

    def draw_axis_x(self, axis_x: Axis) -> None:
        if not axis_x.visible:
            return

        origin_y = self.local_origin_to_screen_coords(self._canvas_pos)[1]
        cx = self._canvas_pos[0]
        cw = self._canvas_size[0]
        color = imgui.get_color_u32_rgba(*axis_x.color)
        thickness = axis_x.thickness

        x1 = cx
        y1 = origin_y
        x2 = cx + cw
        y2 = origin_y
        self._draw_list.add_line(x1, y1, x2, y2, color, thickness)

    def draw_axis_y(self, axis_y: Axis) -> None:
        if not axis_y.visible:
            return

        origin_x = self.local_origin_to_screen_coords(self._canvas_pos)[0]
        cy = self._canvas_pos[1]
        ch = self._canvas_size[1]
        color = imgui.get_color_u32_rgba(*axis_y.color)
        thickness = axis_y.thickness

        x1 = origin_x
        y1 = cy
        x2 = origin_x
        y2 = cy + ch
        self._draw_list.add_line(x1, y1, x2, y2, color, thickness)
