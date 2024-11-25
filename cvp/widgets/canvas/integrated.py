# -*- coding: utf-8 -*-

from typing import List, Optional, Sequence

import imgui

from cvp.flow.datas import Axis
from cvp.flow.datas import Canvas as CanvasProps
from cvp.flow.datas import Grid, Node
from cvp.gl.texture import Texture
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

    def draw_texture(
        self,
        texture: Texture,
        x: float,
        y: float,
        color: Optional[RGBA] = None,
    ) -> None:
        img_id = texture.texture
        img_x = x
        img_y = y
        img_w = texture.width
        img_h = texture.height
        img_roi = img_x, img_y, img_w, img_h
        img_screen_roi = self.canvas_to_screen_roi(img_roi, self._canvas_pos)
        img_screen_p1 = img_screen_roi[0], img_screen_roi[1]
        img_screen_p2 = img_screen_roi[2], img_screen_roi[3]
        img_color = imgui.get_color_u32_rgba(*color) if color is not None else 0
        self._draw_list.add_image(
            img_id,
            img_screen_p1,
            img_screen_p2,
            (0, 0),
            (1, 1),
            img_color,
        )

    def draw_node(self, node: Node) -> None:
        node_roi = self.canvas_to_screen_roi(node.roi, self._canvas_pos)
        x1, y1, x2, y2 = node_roi
        rounding = node.rounding
        flags = node.flags
        thickness = node.thickness
        outline_color = imgui.get_color_u32_rgba(0.2, 0.2, 0.2, 1.0)
        node_color = imgui.get_color_u32_rgba(*node.color)
        self._draw_list.add_rect_filled(x1, y1, x2, y2, outline_color, rounding, flags)
        self._draw_list.add_rect(x1, y1, x2, y2, node_color, rounding, flags, thickness)

    def find_hovering_nodes(self, nodes: Sequence[Node]) -> List[Node]:
        result = list()
        for node in nodes:
            roi = self.canvas_to_screen_roi(node.roi, self._canvas_pos)
            if imgui.is_mouse_hovering_rect(*roi):
                result.append(node)
        return result
