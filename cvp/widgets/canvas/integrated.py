# -*- coding: utf-8 -*-

from typing import Optional, Sequence

import imgui

from cvp.flow.datas import Arc, Axis
from cvp.flow.datas import Canvas as CanvasProps
from cvp.flow.datas import Grid, Node, Style
from cvp.gl.texture import Texture
from cvp.types.colors import RGBA
from cvp.widgets.canvas.controller import CanvasController


class IntegratedCanvas(CanvasController):
    def __init__(self, canvas_props: Optional[CanvasProps] = None):
        super().__init__(canvas_props)

    def fill(self, color: RGBA) -> None:
        filled_color = imgui.get_color_u32_rgba(*color)
        cx, cy = self.canvas_pos
        cw, ch = self.canvas_size
        self.draw_list.add_rect_filled(cx, cy, cx + cw, cy + cy, filled_color)

    def draw_grid_x(self, grid_x: Grid) -> None:
        if not grid_x.visible:
            return

        color = imgui.get_color_u32_rgba(*grid_x.color)
        step = grid_x.step
        thickness = grid_x.thickness
        lines = self.vertical_grid_lines(step)

        for line in lines:
            x1, y1, x2, y2 = line
            self.draw_list.add_line(x1, y1, x2, y2, color, thickness)

    def draw_grid_y(self, grid_y: Grid) -> None:
        if not grid_y.visible:
            return

        color = imgui.get_color_u32_rgba(*grid_y.color)
        step = grid_y.step
        thickness = grid_y.thickness
        lines = self.horizontal_grid_lines(step)

        for line in lines:
            x1, y1, x2, y2 = line
            self.draw_list.add_line(x1, y1, x2, y2, color, thickness)

    def draw_axis_x(self, axis_x: Axis) -> None:
        if not axis_x.visible:
            return

        origin_y = self.local_origin_to_screen_coords()[1]
        cx = self.canvas_pos[0]
        cw = self.canvas_size[0]
        color = imgui.get_color_u32_rgba(*axis_x.color)
        thickness = axis_x.thickness

        x1 = cx
        y1 = origin_y
        x2 = cx + cw
        y2 = origin_y
        self.draw_list.add_line(x1, y1, x2, y2, color, thickness)

    def draw_axis_y(self, axis_y: Axis) -> None:
        if not axis_y.visible:
            return

        origin_x = self.local_origin_to_screen_coords()[0]
        cy = self.canvas_pos[1]
        ch = self.canvas_size[1]
        color = imgui.get_color_u32_rgba(*axis_y.color)
        thickness = axis_y.thickness

        x1 = origin_x
        y1 = cy
        x2 = origin_x
        y2 = cy + ch
        self.draw_list.add_line(x1, y1, x2, y2, color, thickness)

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
        img_screen_roi = self.canvas_to_screen_roi(img_roi)
        img_screen_p1 = img_screen_roi[0], img_screen_roi[1]
        img_screen_p2 = img_screen_roi[2], img_screen_roi[3]
        img_color = imgui.get_color_u32_rgba(*color) if color is not None else 0
        self.draw_list.add_image(
            img_id,
            img_screen_p1,
            img_screen_p2,
            (0, 0),
            (1, 1),
            img_color,
        )

    def is_selected_node(self, node: Node) -> bool:
        if not self.left_button_clicked:
            return False

        roi = self.canvas_to_screen_roi(node.roi)
        return imgui.is_mouse_hovering_rect(*roi)

    def update_nodes_state(self, nodes: Sequence[Node]) -> None:
        for node in nodes:
            node_roi = self.canvas_to_screen_roi(node.roi)
            node.state.screen_roi = node_roi
            node.state.hovering = imgui.is_mouse_hovering_rect(*node_roi)

        if self.hovering and self.left_button_clicked:
            any_selected = False
            for node in nodes:
                if node.state.hovering:
                    node.state.selected = not node.state.selected
                    any_selected = True
                    break
            if not any_selected:
                for node in nodes:
                    node.state.selected = False

    def draw_nodes(self, nodes: Sequence[Node], style: Style) -> None:
        for node in nodes:
            self.draw_node(node, style)

    def draw_node(self, node: Node, style: Style) -> None:
        roi = self.canvas_to_screen_roi(node.roi)
        stroke = style.get_node_stroke(node.state.selected, node.state.hovering)

        fill_color = imgui.get_color_u32_rgba(*node.color)
        stroke_color = imgui.get_color_u32_rgba(*stroke.color)
        thickness = stroke.thickness
        rounding = stroke.rounding
        flags = stroke.flags

        self.draw_list.add_rect_filled(*roi, fill_color, rounding, flags)
        self.draw_list.add_rect(*roi, stroke_color, rounding, flags, thickness)

    def draw_arcs(self, arcs: Sequence[Arc], style: Style) -> None:
        for arc in arcs:
            self.draw_arc(arc, style)

    def draw_arc(self, arc: Arc, style: Style) -> None:
        pass
