# -*- coding: utf-8 -*-

from typing import Final, Optional, Sequence
from weakref import ReferenceType, ref

import imgui

from cvp.flow.datas import Action, Arc, Axis, Graph, Grid, Node, Stream, Style
from cvp.fonts.glyphs.mdi import (
    MDI_ARROW_RIGHT_CIRCLE,
    MDI_ARROW_RIGHT_CIRCLE_OUTLINE,
    MDI_CIRCLE,
    MDI_CIRCLE_OUTLINE,
)
from cvp.gl.texture import Texture
from cvp.imgui.fonts.mapper import FontMapper
from cvp.types.colors import RGBA
from cvp.widgets.canvas.base.controller import CanvasController

FLOW_PIN_N_ICON: Final[str] = MDI_ARROW_RIGHT_CIRCLE_OUTLINE
FLOW_PIN_Y_ICON: Final[str] = MDI_ARROW_RIGHT_CIRCLE
DATA_PIN_N_ICON: Final[str] = MDI_CIRCLE_OUTLINE
DATA_PIN_Y_ICON: Final[str] = MDI_CIRCLE


class GraphCanvas(CanvasController):
    _graph: ReferenceType[Graph]
    _fonts: ReferenceType[FontMapper]

    def __init__(self, graph: Graph, fonts: FontMapper):
        super().__init__()
        self._graph = ref(graph)
        self._fonts = ref(fonts)

    @property
    def graph(self) -> Graph:
        graph = self._graph()
        if graph is None:
            raise ReferenceError("The graph instance has expired")
        return graph

    @property
    def fonts(self) -> FontMapper:
        fonts = self._fonts()
        if fonts is None:
            raise ReferenceError("The fonts instance has expired")
        return fonts

    def process_controllers(self, debugging=False) -> None:
        if result := self.render_controllers(debugging=debugging):
            self.graph.canvas.pan_x = result.pan_x
            self.graph.canvas.pan_y = result.pan_y
            self.graph.canvas.zoom = result.zoom

    def fill(self) -> None:
        graph = self.graph
        color = imgui.get_color_u32_rgba(*graph.color)
        self.draw_list.add_rect_filled(*self.canvas_roi, color)

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

    def draw_node(self, node: Node, style: Style, debug=True) -> None:
        roi = self.canvas_to_screen_roi(node.roi)
        stroke = style.get_node_stroke(node.state.selected, node.state.hovering)

        with self.fonts.normal_icon:
            flow_n_w, flow_n_h = imgui.calc_text_size(FLOW_PIN_N_ICON)
            flow_y_w, flow_y_h = imgui.calc_text_size(FLOW_PIN_Y_ICON)
            data_n_w, data_n_h = imgui.calc_text_size(DATA_PIN_N_ICON)
            data_y_w, data_y_h = imgui.calc_text_size(DATA_PIN_Y_ICON)

        fw = max(flow_y_w, flow_n_w)
        fh = max(flow_y_h, flow_n_h)
        dw = max(data_y_w, data_n_w)
        dh = max(data_y_h, data_n_h)

        flow_inputs = list()
        data_inputs = list()

        flow_outputs = list()
        data_outputs = list()

        input_name_w = 0
        output_name_w = 0

        for pin in node.pins:
            pin_name_w, pin_name_h = imgui.calc_text_size(pin.name)
            if pin.action == Action.flow and pin.stream == Stream.input:
                flow_inputs.append(pin)
                input_name_w = max(input_name_w, pin_name_w)
            elif pin.action == Action.flow and pin.stream == Stream.output:
                flow_outputs.append(pin)
                output_name_w = max(output_name_w, pin_name_w)
            elif pin.action == Action.data and pin.stream == Stream.input:
                data_inputs.append(pin)
                input_name_w = max(input_name_w, pin_name_w)
            elif pin.action == Action.data and pin.stream == Stream.output:
                data_outputs.append(pin)
                output_name_w = max(output_name_w, pin_name_w)
            else:
                assert pin.action == Action.none

        flow_lines = max(len(flow_inputs), len(flow_outputs))
        data_lines = max(len(data_inputs), len(data_outputs))

        fill_color = imgui.get_color_u32_rgba(*node.color)
        stroke_color = imgui.get_color_u32_rgba(*stroke.color)
        thickness = stroke.thickness
        rounding = stroke.rounding
        flags = stroke.flags

        isw = self.item_spacing[0]
        ish = self.item_spacing[1]

        node_name_w, node_name_h = imgui.calc_text_size(node.name)
        # w: width
        # u: user
        # t: top
        # f: flow
        # d: data
        wu = roi[2] - roi[0]
        wt = isw + node_name_w + isw
        wf = isw + fw + isw + input_name_w + isw + output_name_w + isw + fw + isw
        wd = isw + dw + isw + input_name_w + isw + output_name_w + isw + dw + isw
        node_width = max((wu, wt, wf, wd))
        x1, y1, x2, y2 = roi
        x2 = x1 + node_width
        roi = x1, y1, x2, y2

        self.draw_list.add_rect_filled(*roi, fill_color, rounding, flags)
        self.draw_list.add_rect(*roi, stroke_color, rounding, flags, thickness)

        label_color = imgui.get_color_u32_rgba(*style.node_name_color)
        self.draw_list.add_text(x1 + isw, y1 + ish, label_color, node.name)

        node_name_roi = x1, y1, x2, y1 + ish + node_name_h + ish

        flow_h = ish + (fh + ish) * flow_lines
        flow_pin_roi = x1, node_name_roi[3], x2, node_name_roi[3] + flow_h

        data_h = ish + (dh + ish) * data_lines
        data_pin_roi = x1, flow_pin_roi[3], x2, flow_pin_roi[3] + data_h

        if debug:
            self.draw_list.add_rect(*node_name_roi, label_color)
            self.draw_list.add_rect(*flow_pin_roi, label_color)
            self.draw_list.add_rect(*data_pin_roi, label_color)

        with self.fonts.normal_icon:
            for i, pin in enumerate(flow_inputs):
                x1 = flow_pin_roi[0] + isw
                y1 = flow_pin_roi[1] + ish + (fh + ish) * i
                self.draw_list.add_text(x1, y1, label_color, FLOW_PIN_N_ICON)
                with self.fonts.normal_text:
                    self.draw_list.add_text(x1 + fw + isw, y1, label_color, pin.name)

            for i, pin in enumerate(data_inputs):
                x1 = data_pin_roi[0] + isw
                y1 = data_pin_roi[1] + ish + (dh + ish) * i
                self.draw_list.add_text(x1, y1, label_color, DATA_PIN_N_ICON)
                with self.fonts.normal_text:
                    self.draw_list.add_text(x1 + dw + isw, y1, label_color, pin.name)

            for i, pin in enumerate(flow_outputs):
                x1 = flow_pin_roi[2] - isw - fw
                y1 = flow_pin_roi[1] + ish + (fh + ish) * i
                self.draw_list.add_text(x1, y1, label_color, FLOW_PIN_Y_ICON)
                with self.fonts.normal_text:
                    pin_name_w, pin_name_h = imgui.calc_text_size(pin.name)
                    self.draw_list.add_text(
                        x1 - isw - pin_name_w,
                        y1,
                        label_color,
                        pin.name,
                    )

            for i, pin in enumerate(data_outputs):
                x1 = data_pin_roi[2] - isw - dw
                y1 = data_pin_roi[1] + ish + (dh + ish) * i
                self.draw_list.add_text(x1, y1, label_color, DATA_PIN_Y_ICON)
                with self.fonts.normal_text:
                    pin_name_w, pin_name_h = imgui.calc_text_size(pin.name)
                    self.draw_list.add_text(
                        x1 - isw - pin_name_w,
                        y1,
                        label_color,
                        pin.name,
                    )

    def draw_arcs(self, arcs: Sequence[Arc], style: Style) -> None:
        for arc in arcs:
            self.draw_arc(arc, style)

    def draw_arc(self, arc: Arc, style: Style) -> None:
        pass
