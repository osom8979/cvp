# -*- coding: utf-8 -*-

from typing import Final, Optional

import imgui

from cvp.config.sections.flow import FlowAuiConfig
from cvp.config.sections.proxies.flow import SplitTreeProxy
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child
from cvp.imgui.drag_types import DRAG_FLOW_NODE_TYPE
from cvp.imgui.draw_list import get_window_draw_list
from cvp.imgui.menu_item_ex import menu_item
from cvp.imgui.push_style_var import style_item_spacing
from cvp.imgui.text_centered import text_centered
from cvp.logging.logging import logger
from cvp.popups.confirm import ConfirmPopup
from cvp.popups.input_text import InputTextPopup
from cvp.popups.open_file import OpenFilePopup
from cvp.types.override import override
from cvp.variables import (
    AUI_PADDING_HEIGHT,
    AUI_PADDING_WIDTH,
    MAX_SIDEBAR_HEIGHT,
    MAX_SIDEBAR_WIDTH,
    MIN_SIDEBAR_HEIGHT,
    MIN_SIDEBAR_WIDTH,
    MIN_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
)
from cvp.widgets.aui import AuiWindow
from cvp.widgets.canvas.controller import CanvasController
from cvp.widgets.splitter import Splitter
from cvp.windows.flow.bottom import FlowBottomTabs
from cvp.windows.flow.catalogs import Catalogs
from cvp.windows.flow.left import FlowLeftTabs
from cvp.windows.flow.right import FlowRightTabs

_WINDOW_NO_MOVE: Final[int] = imgui.WINDOW_NO_MOVE
_WINDOW_NO_SCROLLBAR: Final[int] = imgui.WINDOW_NO_SCROLLBAR
_WINDOW_NO_RESIZE: Final[int] = imgui.WINDOW_NO_RESIZE
CANVAS_FLAGS: Final[int] = _WINDOW_NO_MOVE | _WINDOW_NO_SCROLLBAR | _WINDOW_NO_RESIZE


class FlowWindow(AuiWindow[FlowAuiConfig]):
    _prev_cursor: Optional[str]

    def __init__(self, context: Context):
        min_width = MIN_WINDOW_WIDTH
        min_height = MIN_WINDOW_HEIGHT
        modifiable_title = False
        min_sidebar_width = MIN_SIDEBAR_WIDTH
        max_sidebar_width = MAX_SIDEBAR_WIDTH
        min_sidebar_height = MIN_SIDEBAR_HEIGHT
        max_sidebar_height = MAX_SIDEBAR_HEIGHT
        padding_width = AUI_PADDING_WIDTH
        padding_height = AUI_PADDING_HEIGHT

        super().__init__(
            context=context,
            window_config=context.config.flow_aui,
            title="Flow",
            closable=True,
            flags=imgui.WINDOW_MENU_BAR,
            min_width=min_width,
            min_height=min_height,
            modifiable_title=modifiable_title,
            min_sidebar_width=min_sidebar_width,
            max_sidebar_width=max_sidebar_width,
            min_sidebar_height=min_sidebar_height,
            max_sidebar_height=max_sidebar_height,
            padding_width=padding_width,
            padding_height=padding_height,
        )

        self._control = CanvasController()
        self._catalogs = Catalogs(context)
        self._left_tabs = FlowLeftTabs(context)
        self._right_tabs = FlowRightTabs(context)
        self._bottom_tabs = FlowBottomTabs(context)

        self._prev_cursor = None
        self._graph_path = str()
        self._node_path = str()

        self._clear_color = 0.5, 0.5, 0.5, 1.0
        self._background = None
        self._enable_context_menu = True

        self._split_tree = SplitTreeProxy(context.config.flow_aui)
        self._tree_splitter = Splitter.from_horizontal(
            "## HSplitterTree",
            value_proxy=self._split_tree,
            min_value=min_sidebar_height,
            negative_delta=True,
        )

        self._new_graph_popup = InputTextPopup(
            title="New graph",
            label="Please enter a graph name:",
            ok="Create",
            cancel="Cancel",
            target=self.on_new_graph_popup,
        )
        self._open_graph_popup = OpenFilePopup(
            title="Open graph file",
            target=self.on_open_file_popup,
        )
        self._confirm_remove = ConfirmPopup(
            title="Remove",
            label="Are you sure you want to remove graph?",
            ok="Remove",
            cancel="No",
            target=self.on_confirm_remove,
        )

        self.register_popup(self._new_graph_popup)
        self.register_popup(self._open_graph_popup)
        self.register_popup(self._confirm_remove)

    @property
    def split_tree(self) -> float:
        return self.window_config.split_tree

    @split_tree.setter
    def split_tree(self, value: float) -> None:
        self.window_config.split_tree = value

    @property
    def current_graph(self):
        return self.context.fm.current_graph

    def on_new_graph_popup(self, name: str) -> None:
        graph = self.context.fm.create_graph(name, append=True, open=True)
        filepath = self.context.home.flows.graph_filepath(graph.uuid)
        if filepath.exists():
            raise FileExistsError(f"Graph file already exists: '{str(filepath)}'")
        self.context.fm.write_graph_yaml(filepath, graph)

    def on_open_file_popup(self, file: str) -> None:
        pass

    def on_confirm_remove(self, value: bool) -> None:
        pass

    @override
    def on_process(self) -> None:
        self.do_process_cursor_events()
        self.on_menu()
        super().on_process()

    def do_process_cursor_events(self):
        if self._prev_cursor == self.context.fm.cursor:
            return

        try:
            if self._prev_cursor:
                self.on_close_graph(self._prev_cursor)

            if self.context.fm.cursor:
                self.on_open_graph(self.context.fm.cursor)
        finally:
            self._prev_cursor = self.context.fm.cursor

    def on_close_graph(self, uuid: str):
        if self.context.debug:
            logger.debug(f"{type(self).__name__}.on_close_graph('{uuid}')")

        graph = self.context.fm.get(uuid)
        if graph is None:
            return

        self.context.save_graph(graph)

    def on_open_graph(self, uuid: str):
        if self.context.debug:
            logger.debug(f"{type(self).__name__}.on_open_graph('{uuid}')")

        graph = self.context.fm.get(uuid)
        if graph is None:
            return

        self._control.canvas = graph.canvas

    def on_menu(self) -> None:
        with imgui.begin_menu_bar() as menu_bar:
            if not menu_bar.opened:
                return

            menus = (
                ("File", self.on_file_menu),
                ("Graph", self.on_graph_menu),
            )

            for name, func in menus:
                with imgui.begin_menu(name) as menu:
                    if menu.opened:
                        func()

    def on_file_menu(self) -> None:
        if imgui.menu_item("New graph")[0]:
            self._new_graph_popup.show()
        # if imgui.menu_item("Open graph file")[0]:
        #     self._open_graph_popup.show()
        # with imgui.begin_menu("Open recent") as recent_menu:
        #     if recent_menu.opened:
        #         if imgui.menu_item("graph1.yml")[0]:
        #             pass
        #         if imgui.menu_item("graph2.yml")[0]:
        #             pass
        # if imgui.menu_item("Save")[0]:
        #     pass
        # if imgui.menu_item("Save As..")[0]:
        #     pass

        imgui.separator()
        has_cursor = self.context.fm.opened
        if imgui.menu_item("Close graph", None, False, enabled=has_cursor)[0]:
            self.context.fm.close_graph()

        imgui.separator()
        if imgui.menu_item("Exit")[0]:
            self.opened = False

    def on_graph_menu(self) -> None:
        if imgui.menu_item("Refresh graphs")[0]:
            self.context.fm.refresh_flow_graphs()

    @override
    def on_process_sidebar_left(self):
        with begin_child("## ChildLeftTop", 0, -self.split_tree):
            self._left_tabs.do_process(self.current_graph)

        with style_item_spacing(0, -1):
            self._tree_splitter.do_process()

        with begin_child("## ChildLeftBottom"):
            with style_item_spacing(0, 0):
                imgui.dummy(0, self.padding_height)
            self._catalogs.on_process()

    @override
    def on_process_sidebar_right(self):
        imgui.text("Canvas controller:")
        self._control.on_process()
        imgui.spacing()

        self._right_tabs.do_process(self._node_path)

    @override
    def on_process_bottom(self):
        self._bottom_tabs.do_process(self._graph_path)

    @override
    def on_process_main(self) -> None:
        if not self.context.fm.opened:
            text_centered("Please select a graph")
            return

        self.begin_child_canvas()
        try:
            self.on_canvas()
            self.on_popup_menu()
        finally:
            imgui.end_child()

    @staticmethod
    def begin_child_canvas() -> None:
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
        imgui.push_style_color(imgui.COLOR_CHILD_BACKGROUND, 0.5, 0.5, 0.5)
        try:
            return begin_child("## Canvas", border=True, flags=CANVAS_FLAGS)
        finally:
            imgui.pop_style_color()
            imgui.pop_style_var()

    def on_canvas(self) -> None:
        mx, my = imgui.get_mouse_pos()
        cx, cy = imgui.get_cursor_screen_pos()
        cw, ch = imgui.get_content_region_available()
        assert isinstance(mx, float)
        assert isinstance(my, float)
        assert isinstance(cx, float)
        assert isinstance(cy, float)
        assert isinstance(cw, float)
        assert isinstance(ch, float)
        mouse_pos = mx, my
        canvas_pos = cx, cy
        canvas_size = cw, ch

        draw_list = get_window_draw_list()
        filled_color = imgui.get_color_u32_rgba(*self._clear_color)
        draw_list.add_rect_filled(cx, cy, cx + cw, cy + cy, filled_color)

        self._control.update(
            cursor_screen_pos=canvas_pos,
            content_region_available=canvas_size,
            has_context_menu=self._enable_context_menu,
        )

        graph = self.current_graph
        if graph is None:
            return

        if graph.grid_x.visible:
            color = imgui.get_color_u32_rgba(*graph.grid_x.color)
            step = graph.grid_x.step
            thickness = graph.grid_x.thickness
            lines = self._control.vertical_grid_lines(step, canvas_pos, canvas_size)
            for line in lines:
                x1, y1, x2, y2 = line
                draw_list.add_line(x1, y1, x2, y2, color, thickness)

        if graph.grid_y.visible:
            color = imgui.get_color_u32_rgba(*graph.grid_y.color)
            step = graph.grid_y.step
            thickness = graph.grid_y.thickness
            lines = self._control.horizontal_grid_lines(step, canvas_pos, canvas_size)
            for line in lines:
                x1, y1, x2, y2 = line
                draw_list.add_line(x1, y1, x2, y2, color, thickness)

        origin_x, origin_y = self._control.world_origin_to_screen_coord(canvas_pos)

        if graph.axis_x.visible:
            color = imgui.get_color_u32_rgba(*graph.axis_x.color)
            thickness = graph.axis_x.thickness
            x1 = cx
            y1 = origin_y
            x2 = cx + cw
            y2 = origin_y
            draw_list.add_line(x1, y1, x2, y2, color, thickness)

        if graph.axis_y.visible:
            color = imgui.get_color_u32_rgba(*graph.axis_y.color)
            thickness = graph.axis_y.thickness
            x1 = origin_x
            y1 = cy
            x2 = origin_x
            y2 = cy + ch
            draw_list.add_line(x1, y1, x2, y2, color, thickness)

        if self._background is not None:
            img_id = self._background.texture_id
            img_x = 0
            img_y = 0
            img_w = self._background.width
            img_h = self._background.height
            img_roi = img_x, img_y, img_w, img_h
            img_screen_roi = self._control.world_to_screen_roi(img_roi, canvas_pos)
            img_screen_p1 = img_screen_roi[0], img_screen_roi[1]
            img_screen_p2 = img_screen_roi[2], img_screen_roi[3]

            alpha = self._control.alpha
            img_color = imgui.get_color_u32_rgba(1.0, 1.0, 1.0, alpha)
            draw_list.add_image(
                img_id,
                img_screen_p1,
                img_screen_p2,
                (0, 0),
                (1, 1),
                img_color,
            )

        for node in graph.nodes:
            node_roi = self._control.world_to_screen_roi(node.roi, canvas_pos)
            x1, y1, x2, y2 = node_roi
            rounding = node.rounding
            flags = node.flags
            thickness = node.thickness
            outline_color = imgui.get_color_u32_rgba(0.2, 0.2, 0.2, 1.0)
            node_color = imgui.get_color_u32_rgba(*node.color)
            draw_list.add_rect_filled(x1, y1, x2, y2, outline_color, rounding, flags)
            draw_list.add_rect(x1, y1, x2, y2, node_color, rounding, flags, thickness)

        # for arc in graph.arcs:
        #     pass

        with imgui.begin_drag_drop_target() as drag_drop_target:
            if drag_drop_target.hovered:
                payload = imgui.accept_drag_drop_payload(DRAG_FLOW_NODE_TYPE)
                if payload is not None:
                    node_path = str(payload, encoding="utf-8")
                    x1, y1 = self._control.screen_to_world_coord(mouse_pos, canvas_pos)
                    x2 = x1 + 100
                    y2 = y1 + 100
                    self.context.fm.add_node(node_path, x1, y1, x2, y2)

    def on_popup_menu(self):
        if not self._enable_context_menu:
            return

        if not imgui.begin_popup_context_window().opened:
            return

        try:
            if menu_item("Reset"):
                self._control.reset()
        finally:
            imgui.end_popup()
