# -*- coding: utf-8 -*-

from typing import List, Optional, Sequence
from weakref import ReferenceType, ref

import imgui

from cvp.flow.datas.arc import Arc
from cvp.flow.datas.graph import Graph
from cvp.flow.datas.node import Node
from cvp.flow.datas.node_pin import NodePin
from cvp.flow.datas.pin import Pin
from cvp.flow.datas.size import FontSize
from cvp.flow.datas.stroke import Stroke
from cvp.flow.datas.style import Style
from cvp.imgui.font_global_scale import font_global_scale
from cvp.imgui.fonts.font import Font
from cvp.imgui.fonts.mapper import FontMapper
from cvp.types.colors import RGBA
from cvp.types.override import override
from cvp.types.shapes import ROI
from cvp.widgets.canvas.controller import CanvasController
from cvp.widgets.canvas.graph.mode import ControlMode


class CanvasGraph(CanvasController):
    _graph_ref: ReferenceType[Graph]
    _fonts_ref: ReferenceType[FontMapper]

    _graph: Optional[Graph]
    _fonts: Optional[FontMapper]

    _connects: List[NodePin]
    _select: Optional[ROI]

    def __init__(self, graph: Graph, fonts: FontMapper):
        super().__init__()
        self._graph_ref = ref(graph)
        self._fonts_ref = ref(fonts)
        self._graph = None
        self._fonts = None

        self._mode = ControlMode.normal
        self._connects = list()
        self._select = None

        self._pan_x.update(graph.canvas.pan_x, no_emit=True)
        self._pan_y.update(graph.canvas.pan_y, no_emit=True)
        self._zoom.update(graph.canvas.zoom, no_emit=True)

    @property
    def is_multi_select_mode(self) -> bool:
        # Pressing the CTRL button switches to 'Multi-node selection mode'
        return self.ctrl_down

    @property
    def is_pan_mode(self) -> bool:
        # Pressing the ALT button switches to 'Canvas Pan Mode'
        return self.alt_down

    @property
    def is_normal_mode(self) -> bool:
        return self._mode == ControlMode.normal

    @property
    def is_node_moving_mode(self) -> bool:
        return self._mode == ControlMode.node_moving

    @property
    def is_pin_connecting_mode(self) -> bool:
        return self._mode == ControlMode.pin_connecting

    @property
    def is_selection_box_mode(self) -> bool:
        return self._mode == ControlMode.selection_box

    @override
    def as_unformatted_text(self) -> str:
        return super().as_unformatted_text() + (
            f"Mode: {self._mode.name}\n"
            f"Connects: {self._connects}\n"
            f"Select: {self._select}\n"
        )

    @property
    def graph(self) -> Graph:
        if self._graph is None:
            raise ReferenceError("The graph instance has expired")
        return self._graph

    @property
    def fonts(self) -> FontMapper:
        if self._fonts is None:
            raise ReferenceError("The fonts instance has expired")
        return self._fonts

    @property
    def opened(self) -> bool:
        return self._graph is not None and self._fonts is not None

    def open(self) -> None:
        if self._graph is not None:
            raise ValueError("Graph already open")
        if self._fonts is not None:
            raise ValueError("Fonts already open")

        assert self._graph is None
        assert self._fonts is None
        self._graph = self._graph_ref()
        self._fonts = self._fonts_ref()

        if self._graph is None:
            self._fonts = None
            raise ReferenceError("The graph instance has expired")

        if self._fonts is None:
            self._graph = None
            raise ReferenceError("The fonts instance has expired")

        assert self._graph is not None
        assert self._fonts is not None

    def close(self) -> None:
        if self._graph is None:
            raise ValueError("Graph instance has expired")
        if self._fonts is None:
            raise ValueError("Fonts instance has expired")

        self._graph = None
        self._fonts = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def reset_controllers(self):
        assert self._graph is not None
        assert self._fonts is not None

        self.pan_x = 0.0
        self.pan_y = 0.0
        self.zoom = 1.0

        canvas = self.graph.canvas
        canvas.pan_x = 0.0
        canvas.pan_y = 0.0
        canvas.zoom = 1.0

    def do_process_controllers(self, debugging=False) -> None:
        assert self._graph is not None
        assert self._fonts is not None

        if result := self.render_controllers(debugging=debugging):
            canvas = self.graph.canvas
            canvas.pan_x = result.pan_x
            canvas.pan_y = result.pan_y
            canvas.zoom = result.zoom

    def do_process_canvas(self) -> None:
        assert self._graph is not None
        assert self._fonts is not None

        if result := self.update_state():
            canvas = self.graph.canvas
            canvas.pan_x = result.pan_x
            canvas.pan_y = result.pan_y
            canvas.zoom = result.zoom

        self.update_nodes_state()
        self.update_arcs_state()

    def draw_graph(self) -> None:
        assert self._graph is not None
        assert self._fonts is not None

        self.fill()
        self.draw_grid_x()
        self.draw_grid_y()
        self.draw_axis_x()
        self.draw_axis_y()

        with font_global_scale(self.zoom):
            self.draw_arcs()
            self.draw_nodes()

        self.draw_pin_connects()
        self.draw_selection_box()

    def fill(self) -> None:
        color = imgui.get_color_u32_rgba(*self.graph.color)
        self._draw_list.add_rect_filled(*self.canvas_roi, color)

    def draw_grid_x(self) -> None:
        grid_x = self.graph.grid_x
        if not grid_x.visible:
            return

        color = imgui.get_color_u32_rgba(*grid_x.color)
        for line in self.vertical_grid_lines(grid_x.step):
            self._draw_list.add_line(*line, color, grid_x.thickness)

    def draw_grid_y(self) -> None:
        grid_y = self.graph.grid_y
        if not grid_y.visible:
            return

        color = imgui.get_color_u32_rgba(*grid_y.color)
        for line in self.horizontal_grid_lines(grid_y.step):
            self._draw_list.add_line(*line, color, grid_y.thickness)

    def draw_axis_x(self) -> None:
        axis_x = self.graph.axis_x
        if not axis_x.visible:
            return

        origin_y = self.local_origin_to_screen_coords()[1]
        color = imgui.get_color_u32_rgba(*axis_x.color)

        x1 = self.cx
        y1 = origin_y
        x2 = self.cx + self.cw
        y2 = origin_y
        self._draw_list.add_line(x1, y1, x2, y2, color, axis_x.thickness)

    def draw_axis_y(self) -> None:
        axis_y = self.graph.axis_y
        if not axis_y.visible:
            return

        origin_x = self.local_origin_to_screen_coords()[0]
        color = imgui.get_color_u32_rgba(*axis_y.color)

        x1 = origin_x
        y1 = self.cy
        x2 = origin_x
        y2 = self.cy + self.ch
        self._draw_list.add_line(x1, y1, x2, y2, color, axis_y.thickness)

    # def draw_texture(
    #     self,
    #     texture: Texture,
    #     x: float,
    #     y: float,
    #     color: Optional[RGBA] = None,
    # ) -> None:
    #     img_id = texture.texture
    #     img_x = x
    #     img_y = y
    #     img_w = texture.width
    #     img_h = texture.height
    #     img_roi = img_x, img_y, img_w, img_h
    #     img_screen_roi = self.canvas_to_screen_roi(img_roi)
    #     img_screen_p1 = img_screen_roi[0], img_screen_roi[1]
    #     img_screen_p2 = img_screen_roi[2], img_screen_roi[3]
    #     img_color = imgui.get_color_u32_rgba(*color) if color is not None else 0
    #     self.draw_list.add_image(
    #         img_id,
    #         img_screen_p1,
    #         img_screen_p2,
    #         (0, 0),
    #         (1, 1),
    #         img_color,
    #     )

    @staticmethod
    def _update_nodes_for_multiple_select(nodes: Sequence[Node]) -> None:
        for node in nodes:
            if node.hovering:
                node.selected = not node.selected
                return

    def _update_pins_single_hovering(self, node: Node) -> None:
        for pin in node.pins:
            icon_x = node.node_pos[0] + pin.icon_pos[0]
            icon_y = node.node_pos[1] + pin.icon_pos[1]
            icon_w = pin.icon_size[0]
            icon_h = pin.icon_size[1]
            icon_roi = icon_x, icon_y, icon_x + icon_w, icon_y + icon_h
            icon_roi = self.canvas_to_screen_roi(icon_roi)
            pin.hovering = imgui.is_mouse_hovering_rect(*icon_roi)
            if pin.hovering:
                return

    def _update_nodes_single_hovering(self, nodes: Sequence[Node]) -> None:
        for node in nodes:
            roi = self.canvas_to_screen_roi(node.node_roi)
            node.hovering = imgui.is_mouse_hovering_rect(*roi)
            if node.hovering:
                self._update_pins_single_hovering(node)
                return

    def update_nodes_state(self) -> None:
        nodes = self.graph.nodes

        self.graph.clear_state()
        self._update_nodes_single_hovering(nodes)

        if self.is_pan_mode:
            # Nodes cannot be selected or dragged during 'Canvas Pan Mode'.
            return

        match self._mode:
            case ControlMode.normal:
                self._update_nodes_state_for_normal()
            case ControlMode.node_moving:
                self._update_nodes_state_for_node_moving()
            case ControlMode.pin_connecting:
                self._update_nodes_state_for_pin_connecting()
            case ControlMode.selection_box:
                self._update_nodes_state_for_selection_box()
            case _:
                assert False, "Inaccessible section"

    def _update_nodes_state_for_normal(self) -> None:
        assert not self.is_pan_mode
        assert self.is_normal_mode

        if self.changed_left_up:
            if self.is_multi_select_mode:
                self.graph.flip_selected_on_hovering_nodes()
            else:
                if self.graph.find_hovering_node() is not None:
                    self.graph.select_on_hovering_nodes()
                else:
                    self.graph.unselect_all_nodes()

        if self.activating and self.start_left_dragging:
            if hovering_node := self.graph.find_hovering_node():
                if hovering_np := self.graph.find_hovering_pin(hovering_node):
                    assert hovering_node == hovering_np.node
                    self._mode = ControlMode.pin_connecting
                    self._connects.clear()
                    self._connects.append(hovering_np)
                elif hovering_node.selected:
                    self._mode = ControlMode.node_moving
                else:
                    self._mode = ControlMode.node_moving
                    if not self.is_multi_select_mode:
                        self.graph.unselect_all_nodes()
                    hovering_node.selected = True
            else:
                self._mode = ControlMode.selection_box
                self._select = self.mx, self.my, self.mx, self.my

    def _update_nodes_state_for_node_moving(self) -> None:
        assert not self.is_pan_mode
        assert self.is_node_moving_mode

        if self.changed_left_up:
            self._mode = ControlMode.normal
        else:
            io = imgui.get_io()
            dx = io.mouse_delta.x / self.zoom
            dy = io.mouse_delta.y / self.zoom
            self.graph.move_on_selected_nodes((dx, dy))

    def _update_nodes_state_for_pin_connecting(self) -> None:
        assert not self.is_pan_mode
        assert self.is_pin_connecting_mode
        assert 1 <= len(self._connects)

        connect_pairs = list()

        if hovering_np := self.graph.find_hovering_pin():
            for conn in self._connects:
                try:
                    pair = self.graph.reorder_connectable_pins(conn, hovering_np)
                    connect_pairs.append(pair)
                except ValueError:
                    connect_pairs.clear()
                    break
            hovering_np.pin.connectable = bool(connect_pairs)

        if self.changed_left_up:
            if connect_pairs:
                for out_conn, in_conn in connect_pairs:
                    self.graph.connect_pins(out_conn, in_conn, no_reorder=True)

            self._mode = ControlMode.normal
            self._connects.clear()

    def _update_nodes_state_for_selection_box(self) -> None:
        assert not self.is_pan_mode
        assert self.is_selection_box_mode
        assert self._select is not None

        x1 = self._select[0]
        y1 = self._select[1]
        x2 = self.mx
        y2 = self.my
        self._select = x1, y1, x2, y2
        x1, y1, x2, y2 = self.screen_to_canvas_roi(self._select)
        left = min(x1, x2)
        right = max(x1, x2)
        top = min(y1, y2)
        bottom = max(y1, y2)

        for node in self.graph.nodes:
            nx1, ny1, nx2, ny2 = node.node_roi
            x_in = left <= nx1 <= right or left <= nx2 <= right
            y_in = top <= ny1 <= bottom or top <= ny2 <= bottom
            node.selected = x_in and y_in

        if self.changed_left_up:
            self._mode = ControlMode.normal
            self._select = None

    def get_pin_color(self, pin: Pin, style: Style) -> RGBA:
        if self.is_pin_connecting_mode:
            if pin.hovering and pin.connectable:
                return style.connect_color
        else:
            if pin.hovering:
                return style.hovering_color

        return style.normal_color

    @staticmethod
    def get_node_stroke(node: Node, style: Style) -> Stroke:
        if node.selected:
            return style.selected_node
        elif node.hovering:
            return style.hovering_node
        else:
            return style.normal_node

    @staticmethod
    def get_text_font(fonts: FontMapper, size: FontSize) -> Font:
        if size == FontSize.normal:
            return fonts.normal_text
        elif size == FontSize.medium:
            return fonts.medium_text
        elif size == FontSize.large:
            return fonts.large_text
        else:
            assert False, "Inaccessible section"

    @staticmethod
    def get_icon_font(fonts: FontMapper, size: FontSize) -> Font:
        if size == FontSize.normal:
            return fonts.normal_icon
        elif size == FontSize.medium:
            return fonts.medium_icon
        elif size == FontSize.large:
            return fonts.large_icon
        else:
            assert False, "Inaccessible section"

    def update_nodes_rois(self) -> None:
        for node in self.graph.nodes:
            self.update_node_roi(node)

    def update_node_roi(self, node: Node) -> None:
        emblem_font = self.get_icon_font(self.fonts, self.graph.style.emblem_size)
        title_font = self.get_text_font(self.fonts, self.graph.style.title_size)
        text_font = self.get_text_font(self.fonts, self.graph.style.text_size)
        icon_font = self.get_icon_font(self.fonts, self.graph.style.icon_size)

        with emblem_font:
            node_emblem_w, node_emblem_h = imgui.calc_text_size(node.emblem)

        with title_font:
            node_name_w, node_name_h = imgui.calc_text_size(node.name)

        title_h = max(node_emblem_h, node_name_h)
        emblem_y_diff = title_h / 2 - node_emblem_h / 2
        title_y_diff = title_h / 2 - node_name_h / 2

        with icon_font:
            flow_n_w, flow_n_h = imgui.calc_text_size(self.graph.style.flow_pin_n_icon)
            flow_y_w, flow_y_h = imgui.calc_text_size(self.graph.style.flow_pin_y_icon)
            data_n_w, data_n_h = imgui.calc_text_size(self.graph.style.data_pin_n_icon)
            data_y_w, data_y_h = imgui.calc_text_size(self.graph.style.data_pin_y_icon)

        iw = max(flow_y_w, flow_n_w, data_y_w, data_n_w)
        ih = max(flow_y_h, flow_n_h, data_y_h, data_n_h)

        with text_font:
            for pin in node.pins:
                pin.icon_size = iw, ih
                pin.name_size = imgui.calc_text_size(pin.name)
            input_name_sizes = [p.name_size for p in node.input_pins]
            output_name_sizes = [p.name_size for p in node.output_pins]

        inw = max(s[0] for s in input_name_sizes)
        inh = max(s[1] for s in input_name_sizes)
        onw = max(s[0] for s in output_name_sizes)
        onh = max(s[1] for s in output_name_sizes)
        pin_name_h = max(inh, onh)

        pin_h = max(ih, inh, onh)
        pin_icon_y_diff = pin_h / 2 - ih / 2
        pin_name_y_diff = pin_h / 2 - pin_name_h / 2

        isw, ish = self.graph.style.item_spacing
        center_padding = isw * 4

        wt = isw + node_emblem_w + isw + node_name_w + isw
        wf = isw + iw + isw + inw + center_padding + onw + isw + iw + isw
        wd = isw + iw + isw + inw + center_padding + onw + isw + iw + isw
        node_w = max((wt, wf, wd))

        header_h = ish + title_h + ish
        flow_h = ish + (ih + ish) * node.flow_lines
        data_h = ish + (ih + ish) * node.data_lines
        node_h = header_h + flow_h + data_h

        node_emblem_x = isw
        node_emblem_y = ish + emblem_y_diff
        node.emblem_pos = node_emblem_x, node_emblem_y
        node.emblem_size = node_emblem_w, node_emblem_h

        node_name_x = node.emblem_pos[0] + node.emblem_size[0] + isw
        node_name_y = ish + title_y_diff
        node.name_pos = node_name_x, node_name_y
        node.name_size = node_name_w, node_name_h

        node.node_pos = 0.0, 0.0
        node.node_size = node_w, node_h

        for i, pin in enumerate(node.flow_inputs):
            icon_x = isw
            icon_y = header_h + ish + (ih + ish) * i
            pin.icon_pos = icon_x, icon_y + pin_icon_y_diff

            name_x = icon_x + pin.icon_size[0] + isw
            name_y = icon_y + pin_name_y_diff
            pin.name_pos = name_x, name_y

        for i, pin in enumerate(node.data_inputs):
            icon_x = isw
            icon_y = header_h + flow_h + ish + (ih + ish) * i
            pin.icon_pos = icon_x, icon_y + pin_icon_y_diff

            name_x = icon_x + pin.icon_size[0] + isw
            name_y = icon_y + pin_name_y_diff
            pin.name_pos = name_x, name_y

        for i, pin in enumerate(node.flow_outputs):
            icon_x = node_w - isw - iw
            icon_y = header_h + ish + (ih + ish) * i
            pin.icon_pos = icon_x, icon_y + pin_icon_y_diff

            name_x = icon_x - isw - pin.name_size[0]
            name_y = icon_y + pin_name_y_diff
            pin.name_pos = name_x, name_y

        for i, pin in enumerate(node.data_outputs):
            icon_x = node_w - isw - iw
            icon_y = header_h + flow_h + ish + (ih + ish) * i
            pin.icon_pos = icon_x, icon_y + pin_icon_y_diff

            name_x = icon_x - isw - pin.name_size[0]
            name_y = icon_y + pin_name_y_diff
            pin.name_pos = name_x, name_y

    def draw_nodes(self) -> None:
        for node in reversed(self.graph.nodes):
            self.draw_node(node)

    def draw_node(self, node: Node) -> None:
        node_roi = self.canvas_to_screen_roi(node.node_roi)
        style = self.graph.style
        stroke = self.get_node_stroke(node, style)

        fill_color = imgui.get_color_u32_rgba(*node.color)
        stroke_color = imgui.get_color_u32_rgba(*stroke.color)
        label_color = imgui.get_color_u32_rgba(*style.normal_color)
        layout_color = imgui.get_color_u32_rgba(*style.layout_color)

        thickness = stroke.thickness
        rounding = stroke.rounding
        flags = stroke.flags

        self._draw_list.add_rect_filled(*node_roi, fill_color, rounding, flags)
        self._draw_list.add_rect(*node_roi, stroke_color, rounding, flags, thickness)

        graph = self.graph
        fonts = self.fonts

        assert isinstance(graph, Graph)
        assert isinstance(fonts, FontMapper)

        emblem_font = self.get_icon_font(fonts, graph.style.emblem_size)
        title_font = self.get_text_font(fonts, graph.style.title_size)
        text_font = self.get_text_font(fonts, graph.style.text_size)
        icon_font = self.get_icon_font(fonts, graph.style.icon_size)

        nx = node_roi[0]
        ny = node_roi[1]
        zoom = self.zoom

        with emblem_font:
            x1 = nx + node.emblem_pos[0] * zoom
            y1 = ny + node.emblem_pos[1] * zoom
            self._draw_list.add_text(x1, y1, label_color, node.emblem)
            if graph.style.show_layout:
                x2 = x1 + node.emblem_size[0] * zoom
                y2 = y1 + node.emblem_size[1] * zoom
                self._draw_list.add_rect(x1, y1, x2, y2, layout_color)

        with title_font:
            x1 = nx + node.name_pos[0] * zoom
            y1 = ny + node.name_pos[1] * zoom
            self._draw_list.add_text(x1, y1, label_color, node.name)
            if graph.style.show_layout:
                x2 = x1 + node.name_size[0] * zoom
                y2 = y1 + node.name_size[1] * zoom
                self._draw_list.add_rect(x1, y1, x2, y2, layout_color)

        with icon_font:
            flow_pin_n_icon = graph.style.flow_pin_n_icon
            flow_pin_y_icon = graph.style.flow_pin_y_icon

            for pin in node.flow_pins:
                x1 = nx + pin.icon_pos[0] * zoom
                y1 = ny + pin.icon_pos[1] * zoom
                pin_icon = flow_pin_y_icon if pin.connected else flow_pin_n_icon
                pin_rgba = self.get_pin_color(pin, graph.style)
                pin_color = imgui.get_color_u32_rgba(*pin_rgba)
                self._draw_list.add_text(x1, y1, pin_color, pin_icon)
                if graph.style.show_layout:
                    x2 = x1 + pin.icon_size[0] * zoom
                    y2 = y1 + pin.icon_size[1] * zoom
                    self._draw_list.add_rect(x1, y1, x2, y2, layout_color)

            data_pin_n_icon = graph.style.data_pin_n_icon
            data_pin_y_icon = graph.style.data_pin_y_icon

            for pin in node.data_pins:
                x1 = nx + pin.icon_pos[0] * zoom
                y1 = ny + pin.icon_pos[1] * zoom
                pin_icon = data_pin_y_icon if pin.connected else data_pin_n_icon
                pin_rgba = self.get_pin_color(pin, graph.style)
                pin_color = imgui.get_color_u32_rgba(*pin_rgba)
                self._draw_list.add_text(x1, y1, pin_color, pin_icon)
                if graph.style.show_layout:
                    x2 = x1 + pin.icon_size[0] * zoom
                    y2 = y1 + pin.icon_size[1] * zoom
                    self._draw_list.add_rect(x1, y1, x2, y2, layout_color)

        with text_font:
            for pin in node.pins:
                x1 = nx + pin.name_pos[0] * zoom
                y1 = ny + pin.name_pos[1] * zoom
                self._draw_list.add_text(x1, y1, label_color, pin.name)
                if graph.style.show_layout:
                    x2 = x1 + pin.name_size[0] * zoom
                    y2 = y1 + pin.name_size[1] * zoom
                    self._draw_list.add_rect(x1, y1, x2, y2, layout_color)

    def update_arcs_state(self) -> None:
        for arc in self.graph.arcs:
            self.update_arc_state(arc)

    def update_arc_state(self, arc: Arc) -> None:
        if arc.output is None:
            for node in self.graph.nodes:
                if pin := node.find_output_pin(arc.uuid):
                    arc.output = NodePin(node, pin)
                    break

        if arc.input is None:
            for node in self.graph.nodes:
                if pin := node.find_input_pin(arc.uuid):
                    arc.input = NodePin(node, pin)
                    break

    def draw_arcs(self) -> None:
        for arc in self.graph.arcs:
            assert arc.output is not None
            assert arc.input is not None
            self.draw_arc(arc)

    def draw_arc(self, arc: Arc) -> None:
        assert arc.output is not None
        snx, sny = arc.output.node.node_pos
        six, siy = arc.output.pin.icon_pos
        siw, sih = arc.output.pin.icon_size
        sx = snx + six + siw / 2
        sy = sny + siy + sih / 2
        x1, y1 = self.canvas_to_screen_coords((sx, sy))

        assert arc.input is not None
        enx, eny = arc.input.node.node_pos
        eix, eiy = arc.input.pin.icon_pos
        eiw, eih = arc.input.pin.icon_size
        ex = enx + eix + eiw / 2
        ey = eny + eiy + eih / 2
        x2, y2 = self.canvas_to_screen_coords((ex, ey))

        color = imgui.get_color_u32_rgba(*self.graph.style.arc_color)
        thickness = self.graph.style.arc_thickness
        self._draw_list.add_line(x1, y1, x2, y2, color, thickness)

    def draw_pin_connect(self, connect: NodePin) -> None:
        node = connect.node
        pin = connect.pin

        node_roi = self.canvas_to_screen_roi(node.node_roi)
        nx = node_roi[0]
        ny = node_roi[1]
        zoom = self.zoom
        x1 = nx + pin.icon_pos[0] * zoom + pin.icon_size[0] * zoom / 2
        y1 = ny + pin.icon_pos[1] * zoom + pin.icon_size[1] * zoom / 2
        mx, my = self._mouse_pos

        color = imgui.get_color_u32_rgba(*self.graph.style.pin_connection_color)
        thickness = self.graph.style.pin_connection_thickness
        self._draw_list.add_line(x1, y1, mx, my, color, thickness)

    def draw_pin_connects(self) -> None:
        if not self.is_pin_connecting_mode:
            return

        for connect in self._connects:
            self.draw_pin_connect(connect)

    def draw_selection_box(self) -> None:
        if not self.is_selection_box_mode:
            return

        assert self._select is not None
        x1, y1, x2, y2 = self._select
        color = imgui.get_color_u32_rgba(*self.graph.style.selection_box_color)
        thickness = self.graph.style.selection_box_thickness
        self._draw_list.add_rect_filled(x1, y1, x2, y2, color)
        self._draw_list.add_rect(x1, y1, x2, y2, color, 0.0, 0, thickness)