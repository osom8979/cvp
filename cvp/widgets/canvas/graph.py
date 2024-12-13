# -*- coding: utf-8 -*-

from typing import Final, Optional, Sequence
from weakref import ReferenceType, ref

import imgui

from cvp.flow.datas import Arc, FontSize, Graph, Node, Stroke, Style
from cvp.fonts.glyphs.mdi import (
    MDI_ARROW_RIGHT_CIRCLE,
    MDI_ARROW_RIGHT_CIRCLE_OUTLINE,
    MDI_CIRCLE,
    MDI_CIRCLE_OUTLINE,
)
from cvp.imgui.fonts.font import Font
from cvp.imgui.fonts.mapper import FontMapper
from cvp.renderer.widget.interface import WidgetInterface
from cvp.types.override import override
from cvp.widgets.canvas.controller.controller import CanvasController

FLOW_PIN_N_ICON: Final[str] = MDI_ARROW_RIGHT_CIRCLE_OUTLINE
FLOW_PIN_Y_ICON: Final[str] = MDI_ARROW_RIGHT_CIRCLE
DATA_PIN_N_ICON: Final[str] = MDI_CIRCLE_OUTLINE
DATA_PIN_Y_ICON: Final[str] = MDI_CIRCLE


class GraphCanvas(CanvasController, WidgetInterface):
    _graph_ref: ReferenceType[Graph]
    _fonts_ref: ReferenceType[FontMapper]

    _graph: Optional[Graph]
    _fonts: Optional[FontMapper]

    def __init__(self, graph: Graph, fonts: FontMapper):
        super().__init__()
        self._graph_ref = ref(graph)
        self._fonts_ref = ref(fonts)
        self._graph = None
        self._fonts = None

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

    def do_process_controllers(self, debugging=False) -> None:
        if result := self.render_controllers(debugging=debugging):
            self.graph.canvas.pan_x = result.pan_x
            self.graph.canvas.pan_y = result.pan_y
            self.graph.canvas.zoom = result.zoom

    def do_process(self) -> None:
        self.open()
        try:
            self.on_process()
        finally:
            self.close()

    @override
    def on_process(self) -> None:
        assert self._graph is not None
        assert self._fonts is not None

        self.control()
        self.update_nodes_state()

        self.fill()
        self.draw_grid_x()
        self.draw_grid_y()
        self.draw_axis_x()
        self.draw_axis_y()

        self.draw_nodes()
        self.draw_arcs()

    def fill(self) -> None:
        color = imgui.get_color_u32_rgba(*self.graph.color)
        self.draw_list.add_rect_filled(*self.canvas_roi, color)

    def draw_grid_x(self) -> None:
        grid_x = self.graph.grid_x
        if not grid_x.visible:
            return

        color = imgui.get_color_u32_rgba(*grid_x.color)
        for line in self.vertical_grid_lines(grid_x.step):
            self.draw_list.add_line(*line, color, grid_x.thickness)

    def draw_grid_y(self) -> None:
        grid_y = self.graph.grid_y
        if not grid_y.visible:
            return

        color = imgui.get_color_u32_rgba(*grid_y.color)
        for line in self.horizontal_grid_lines(grid_y.step):
            self.draw_list.add_line(*line, color, grid_y.thickness)

    def draw_axis_x(self) -> None:
        axis_x = self.graph.axis_x
        if not axis_x.visible:
            return

        origin_y = self.local_origin_to_screen_coords()[1]
        cx = self.canvas_pos[0]
        cw = self.canvas_size[0]
        color = imgui.get_color_u32_rgba(*axis_x.color)

        x1 = cx
        y1 = origin_y
        x2 = cx + cw
        y2 = origin_y
        self.draw_list.add_line(x1, y1, x2, y2, color, axis_x.thickness)

    def draw_axis_y(self) -> None:
        axis_y = self.graph.axis_y
        if not axis_y.visible:
            return

        origin_x = self.local_origin_to_screen_coords()[0]
        cy = self.canvas_pos[1]
        ch = self.canvas_size[1]
        color = imgui.get_color_u32_rgba(*axis_y.color)

        x1 = origin_x
        y1 = cy
        x2 = origin_x
        y2 = cy + ch
        self.draw_list.add_line(x1, y1, x2, y2, color, axis_y.thickness)

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

    # def is_selected_node(self, node: Node) -> bool:
    #     if not self.left_clicked:
    #         return False
    #     roi = self.canvas_to_screen_roi(node.roi)
    #     return imgui.is_mouse_hovering_rect(*roi)

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

            x1, y1, x2, y2 = node.node_roi
            x1 += dx
            y1 += dy
            x2 += dx
            y2 += dy
            node.node_roi = x1, y1, x2, y2

    def update_nodes_state(self) -> None:
        nodes = self.graph.nodes
        any_selected_hovering = False

        for node in nodes:
            node_roi = self.canvas_to_screen_roi(node.node_roi)
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

    def draw_nodes(self) -> None:
        for node in self.graph.nodes:
            self.draw_node(node)

    @staticmethod
    def get_node_stroke(node: Node, style: Style) -> Stroke:
        if node.state.selected:
            return style.selected_node
        elif node.state.hovering:
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

    def update_node_rois(self, node: Node) -> None:
        graph = self._graph_ref()
        fonts = self._fonts_ref()

        if graph is None:
            raise ReferenceError("The graph instance has expired")
        if fonts is None:
            raise ReferenceError("The fonts instance has expired")

        assert isinstance(graph, Graph)
        assert isinstance(fonts, FontMapper)
        emblem_font = self.get_icon_font(fonts, graph.style.emblem_size)
        title_font = self.get_text_font(fonts, graph.style.title_size)
        text_font = self.get_text_font(fonts, graph.style.text_size)
        icon_font = self.get_icon_font(fonts, graph.style.icon_size)

        with emblem_font:
            node_emblem_w, node_emblem_h = imgui.calc_text_size(node.emblem)

        with title_font:
            node_name_w, node_name_h = imgui.calc_text_size(node.name)

        title_h = max(node_emblem_h, node_name_h)
        emblem_y_diff = title_h / 2 - node_emblem_h / 2
        title_y_diff = title_h / 2 - node_name_h / 2

        with icon_font:
            flow_n_w, flow_n_h = imgui.calc_text_size(graph.style.flow_pin_n_icon)
            flow_y_w, flow_y_h = imgui.calc_text_size(graph.style.flow_pin_y_icon)
            data_n_w, data_n_h = imgui.calc_text_size(graph.style.data_pin_n_icon)
            data_y_w, data_y_h = imgui.calc_text_size(graph.style.data_pin_y_icon)

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

        isw, ish = graph.style.item_spacing
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

        self.draw_list.add_rect_filled(*node_roi, fill_color, rounding, flags)
        self.draw_list.add_rect(*node_roi, stroke_color, rounding, flags, thickness)

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

        with emblem_font:
            x1 = nx + node.emblem_pos[0]
            y1 = ny + node.emblem_pos[1]
            self.draw_list.add_text(x1, y1, label_color, node.emblem)
            if graph.style.show_layout:
                x2 = x1 + node.emblem_size[0]
                y2 = y1 + node.emblem_size[1]
                self.draw_list.add_rect(x1, y1, x2, y2, layout_color)

        with title_font:
            x1 = nx + node.name_pos[0]
            y1 = ny + node.name_pos[1]
            self.draw_list.add_text(x1, y1, label_color, node.name)
            if graph.style.show_layout:
                x2 = x1 + node.name_size[0]
                y2 = y1 + node.name_size[1]
                self.draw_list.add_rect(x1, y1, x2, y2, layout_color)

        with icon_font:
            flow_pin_n_icon = graph.style.flow_pin_n_icon
            # flow_pin_y_icon = graph.style.flow_pin_y_icon

            for pin in node.flow_pins:
                x1 = nx + pin.icon_pos[0]
                y1 = ny + pin.icon_pos[1]
                self.draw_list.add_text(x1, y1, label_color, flow_pin_n_icon)
                if graph.style.show_layout:
                    x2 = x1 + pin.icon_size[0]
                    y2 = y1 + pin.icon_size[1]
                    self.draw_list.add_rect(x1, y1, x2, y2, layout_color)

            data_pin_n_icon = graph.style.data_pin_n_icon
            # data_pin_y_icon = graph.style.data_pin_y_icon

            for pin in node.data_pins:
                x1 = nx + pin.icon_pos[0]
                y1 = ny + pin.icon_pos[1]
                self.draw_list.add_text(x1, y1, label_color, data_pin_n_icon)
                if graph.style.show_layout:
                    x2 = x1 + pin.icon_size[0]
                    y2 = y1 + pin.icon_size[1]
                    self.draw_list.add_rect(x1, y1, x2, y2, layout_color)

        with text_font:
            for pin in node.pins:
                x1 = nx + pin.name_pos[0]
                y1 = ny + pin.name_pos[1]
                self.draw_list.add_text(x1, y1, label_color, pin.name)
                if graph.style.show_layout:
                    x2 = x1 + pin.name_size[0]
                    y2 = y1 + pin.name_size[1]
                    self.draw_list.add_rect(x1, y1, x2, y2, layout_color)

    def draw_arcs(self) -> None:
        for arc in self.graph.arcs:
            self.draw_arc(arc)

    def draw_arc(self, arc: Arc) -> None:
        pass
