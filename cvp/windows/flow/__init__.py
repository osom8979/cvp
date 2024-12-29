# -*- coding: utf-8 -*-

from typing import Dict, Final, Optional

import imgui

from cvp.config.sections.flow import FlowAuiConfig
from cvp.config.sections.proxies.flow import SplitTreeProxy
from cvp.context.context import Context
from cvp.flow.datas.graph import Graph
from cvp.imgui.begin_child import begin_child
from cvp.imgui.drag_types import DRAG_FLOW_NODE_TYPE
from cvp.imgui.fonts.mapper import FontMapper
from cvp.imgui.menu_item_ex import menu_item
from cvp.imgui.push_style_var import style_item_spacing
from cvp.imgui.text_centered import text_centered
from cvp.logging.logging import logger
from cvp.popups.confirm import ConfirmPopup
from cvp.popups.input_text import InputTextPopup
from cvp.popups.open_file import OpenFilePopup
from cvp.types.override import override
from cvp.variables import MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH
from cvp.widgets.aui import AuiWindow
from cvp.widgets.canvas.graph import CanvasGraph
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
    _canvases: Dict[str, CanvasGraph]
    _prev_cursor: Optional[str]

    def __init__(self, context: Context, fonts: FontMapper):
        super().__init__(
            context=context,
            window_config=context.config.flow_aui,
            title="Flow",
            closable=True,
            flags=imgui.WINDOW_MENU_BAR,
            min_width=MIN_WINDOW_WIDTH,
            min_height=MIN_WINDOW_HEIGHT,
            modifiable_title=False,
        )

        self._fonts = fonts
        self._canvases = dict()
        self._catalogs = Catalogs(context)
        self._left_tabs = FlowLeftTabs(context, fonts)
        self._right_tabs = FlowRightTabs(context, fonts)
        self._bottom_tabs = FlowBottomTabs(context)

        self._prev_cursor = None

        self._split_tree = SplitTreeProxy(context.config.flow_aui)
        self._tree_splitter = Splitter.from_horizontal(
            "##HSplitterTree",
            value_proxy=self._split_tree,
            min_value=context.config.flow_aui.min_split_tree,
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
    def current_graph(self) -> Optional[Graph]:
        return self.context.fm.current_graph

    @property
    def current_canvas(self) -> Optional[CanvasGraph]:
        graph = self.current_graph
        if graph is None:
            return None

        canvas = self._canvases.get(graph.uuid)
        if canvas is None:
            canvas = CanvasGraph(graph, self._fonts)
            self._canvases[graph.uuid] = canvas

        assert canvas is not None
        assert isinstance(canvas, CanvasGraph)
        return canvas

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
            logger.debug(f"{type(self).__name__}.('{uuid}')")

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

        # TODO: Initialize canvas properties

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
        if canvas := self.current_canvas:
            with canvas:
                canvas.do_process_controllers(debugging=self.context.debug)
        imgui.spacing()
        self._right_tabs.do_process(self.current_graph)

    @override
    def on_process_bottom(self):
        self._bottom_tabs.do_process(self.current_graph)

    @override
    def on_process_main(self) -> None:
        if not self.context.fm.opened:
            text_centered("Please select a graph")
            return

        self.begin_child_canvas()
        try:
            self.on_canvas()
        finally:
            imgui.end_child()

    @staticmethod
    def begin_child_canvas() -> None:
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
        imgui.push_style_color(imgui.COLOR_CHILD_BACKGROUND, 0.5, 0.5, 0.5)
        try:
            return begin_child("##Canvas", border=True, flags=CANVAS_FLAGS)
        finally:
            imgui.pop_style_color()
            imgui.pop_style_var()

    def on_canvas(self) -> None:
        canvas = self.current_canvas
        if canvas is None:
            return

        with canvas:
            canvas.do_process_canvas()

        with imgui.begin_drag_drop_target() as drag_drop_target:
            if drag_drop_target.hovered:
                payload = imgui.accept_drag_drop_payload(DRAG_FLOW_NODE_TYPE)
                if payload is not None:
                    node_path = str(payload, encoding="utf-8")
                    node = self.context.fm.add_node(node_path)
                    with canvas:
                        canvas.update_node_roi(node)
                    node.node_pos = canvas.mouse_to_canvas_coords()

        if imgui.begin_popup_context_window().opened:
            try:
                if menu_item("Reset"):
                    with canvas:
                        canvas.reset_controllers()
            finally:
                imgui.end_popup()

        with canvas:
            canvas.draw_graph()
