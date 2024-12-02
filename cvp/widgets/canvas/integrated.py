# -*- coding: utf-8 -*-

from typing import Optional, Sequence

import imgui

from cvp.flow.datas import Arc, Axis
from cvp.flow.datas import Canvas as CanvasProps
from cvp.flow.datas import Grid, Node, Style
from cvp.gl.texture import Texture
from cvp.imgui.fonts.mapper import FontMapper
from cvp.types.colors import RGBA
from cvp.widgets.canvas.controller import CanvasController


class IntegratedCanvas(CanvasController):
    def __init__(
        self,
        fonts: FontMapper,
        canvas_props: Optional[CanvasProps] = None,
    ):
        super().__init__(canvas_props)
        self.fonts = fonts

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
        if not self.left_clicked:
            return False

        roi = self.canvas_to_screen_roi(node.roi)
        return imgui.is_mouse_hovering_rect(*roi)

    @staticmethod
    def _find_hovering_single_node(nodes: Sequence[Node]) -> Optional[Node]:
        for node in nodes:
            if node.state.hovering:
                return node
        return None

    @staticmethod
    def _update_nodes_single_select(nodes: Sequence[Node], selected_node: Node) -> None:
        for node in nodes:
            node.state.selected = selected_node == node

    @staticmethod
    def _update_nodes_all_unselect(nodes: Sequence[Node]) -> None:
        for node in nodes:
            node.state.selected = False

    def _update_nodes_for_single_select(self, nodes: Sequence[Node]) -> None:
        if selected_node := self._find_hovering_single_node(nodes):
            self._update_nodes_single_select(nodes, selected_node)
        else:
            self._update_nodes_all_unselect(nodes)

    @staticmethod
    def _update_nodes_for_multiple_select(nodes: Sequence[Node]) -> None:
        for node in nodes:
            if node.state.hovering:
                node.state.selected = not node.state.selected
                break

    def _update_nodes_for_moving(self, nodes: Sequence[Node]) -> None:
        io = imgui.get_io()
        dx = io.mouse_delta.x / self.zoom
        dy = io.mouse_delta.y / self.zoom

        for node in nodes:
            if not node.state.selected:
                continue

            x1, y1, x2, y2 = node.roi
            x1 += dx
            y1 += dy
            x2 += dx
            y2 += dy
            node.roi = x1, y1, x2, y2

    def update_nodes_state(self, nodes: Sequence[Node]) -> None:
        any_selected_hovering = False

        for node in nodes:
            node_roi = self.canvas_to_screen_roi(node.roi)
            node.state.screen_roi = node_roi
            node.state.hovering = imgui.is_mouse_hovering_rect(*node_roi)
            if node.state.hovering and node.state.selected:
                any_selected_hovering = True

        if self.is_pan_mode:
            # Nodes cannot be selected or dragged during 'Canvas Pan Mode'.
            return

        node_moving = any_selected_hovering and self.activating and self.left_dragging
        if node_moving:
            self._update_nodes_for_moving(nodes)
            return

        if self.prev_left_dragging:
            # When the node drag (movement) is finished, the mouse up event is
            # necessarily fired. Therefore, we check the drag state of the previous
            # frame to prevent the node from being selected.
            return

        if self.left_up:
            if self.ctrl_down:
                self._update_nodes_for_multiple_select(nodes)
            else:
                self._update_nodes_for_single_select(nodes)

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

        name_size = imgui.calc_text_size(node.name)

        x1, y1, x2, y2 = roi
        label_color = imgui.get_color_u32_rgba(*style.node_name_color)
        self.draw_list.add_text(x1, y1, label_color, node.name)

        flow_y_size = imgui.calc_text_size(style.flow_pin_y_icon)
        flow_n_size = imgui.calc_text_size(style.flow_pin_n_icon)
        data_y_size = imgui.calc_text_size(style.data_pin_y_icon)
        data_n_size = imgui.calc_text_size(style.data_pin_n_icon)
        assert flow_y_size == flow_n_size
        assert data_y_size == data_n_size
        x2 -= flow_n_size[0]

        y1 += name_size[1]
        self.draw_list.add_text(x1, y1, label_color, style.flow_pin_y_icon)
        self.draw_list.add_text(x2, y1, label_color, style.flow_pin_n_icon)

        y1 += data_y_size[1]
        self.draw_list.add_text(x1, y1, label_color, style.data_pin_y_icon)
        self.draw_list.add_text(x2, y1, label_color, style.data_pin_n_icon)

    def draw_arcs(self, arcs: Sequence[Arc], style: Style) -> None:
        for arc in arcs:
            self.draw_arc(arc, style)

    def draw_arc(self, arc: Arc, style: Style) -> None:
        pass
