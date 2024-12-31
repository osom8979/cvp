# -*- coding: utf-8 -*-

from typing import Final

import imgui

from cvp.config.sections.flow import FlowAuiConfig
from cvp.config.sections.proxies.flow import SplitTreeProxy
from cvp.context.context import Context
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
from cvp.windows.flow.cursor import FlowCursor
from cvp.windows.flow.left import FlowLeftTabs
from cvp.windows.flow.right import FlowRightTabs

_WINDOW_NO_MOVE: Final[int] = imgui.WINDOW_NO_MOVE
_WINDOW_NO_SCROLLBAR: Final[int] = imgui.WINDOW_NO_SCROLLBAR
_WINDOW_NO_RESIZE: Final[int] = imgui.WINDOW_NO_RESIZE
_CANVAS_FLAGS: Final[int] = _WINDOW_NO_MOVE | _WINDOW_NO_SCROLLBAR | _WINDOW_NO_RESIZE


class FlowWindow(AuiWindow[FlowAuiConfig]):
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
        self._cursor = FlowCursor(fonts)
        self._catalogs = Catalogs(context)
        self._left_tabs = FlowLeftTabs(context, fonts, self._cursor)
        self._right_tabs = FlowRightTabs(context, fonts, self._cursor)
        self._bottom_tabs = FlowBottomTabs(context, fonts, self._cursor)

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

    def on_new_graph_popup(self, name: str) -> None:
        graph = self.context.fm.create_graph(name, append=True)
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
        self.on_menu()
        super().on_process()

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
        if menu_item("New graph"):
            self.show_new_graph_popup()

        # if menu_item("Open graph file"):
        #     self._open_graph_popup.show()
        # with imgui.begin_menu("Open recent") as recent_menu:
        #     if recent_menu.opened:
        #         if menu_item("graph1.yml"):
        #             pass
        #         if menu_item("graph2.yml"):
        #             pass
        # if menu_item("Save"):
        #     pass
        # if menu_item("Save As.."):
        #     pass

        imgui.separator()
        if menu_item("Close graph", enabled=self._cursor.opened):
            self.close_graph()

        imgui.separator()
        if menu_item("Exit"):
            self.close()

    def on_graph_menu(self) -> None:
        if menu_item("Refresh graphs"):
            self.refresh_graphs()

    def show_new_graph_popup(self) -> None:
        self._new_graph_popup.show()

    def close_graph(self):
        graph = self._cursor.graph
        if graph is None:
            return

        if self.context.debug:
            logger.debug(f"Close the flow graph: '{graph.uuid}'")

        try:
            self.context.save_graph(graph)
            logger.info(f"The flow graph was successfully saved: '{graph.uuid}'")
        except BaseException as e:
            logger.error(f"Failed to save the flow graph: '{graph.uuid}' -> '{e}'")
        finally:
            self._cursor.close()

    def refresh_graphs(self) -> None:
        graph_uuid_stash = str()

        if graph := self._cursor.graph:
            graph_uuid_stash = graph.uuid

        self.context.fm.clear()
        self._cursor.clear()

        try:
            self.context.fm.refresh_flow_graphs()
        except BaseException as e:
            logger.error(e)

        if graph_uuid_stash:
            if graph := self.context.fm.get(graph_uuid_stash):
                self._cursor.open(graph)

    @override
    def on_process_sidebar_left(self):
        with begin_child("## ChildLeftTop", 0, -self.split_tree):
            self._left_tabs.do_process(self._cursor.graph)

        with style_item_spacing(0, -1):
            self._tree_splitter.do_process()

        with begin_child("## ChildLeftBottom"):
            with style_item_spacing(0, 0):
                imgui.dummy(0, self.padding_height)
            self._catalogs.on_process()

    @override
    def on_process_sidebar_right(self):
        imgui.text("Canvas controller:")
        if canvas := self._cursor.canvas:
            with canvas:
                canvas.do_process_controllers(debugging=self.context.debug)
        imgui.spacing()
        self._right_tabs.do_process(self._cursor.graph)

    @override
    def on_process_bottom(self):
        self._bottom_tabs.do_process(self._cursor.graph)

    @override
    def on_process_main(self) -> None:
        canvas = self._cursor.canvas
        if canvas is None:
            text_centered("Please select a graph")
            return

        self.begin_child_canvas()
        try:
            with canvas:
                self.on_canvas(canvas)
        finally:
            imgui.end_child()

    @staticmethod
    def begin_child_canvas() -> None:
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
        imgui.push_style_color(imgui.COLOR_CHILD_BACKGROUND, 0.5, 0.5, 0.5)
        try:
            return begin_child("##Canvas", border=True, flags=_CANVAS_FLAGS)
        finally:
            imgui.pop_style_color()
            imgui.pop_style_var()

    def on_canvas(self, canvas: CanvasGraph) -> None:
        assert canvas.opened
        canvas.do_process_canvas()

        with imgui.begin_drag_drop_target() as target:
            if target.hovered:
                if payload := imgui.accept_drag_drop_payload(DRAG_FLOW_NODE_TYPE):
                    node_path = str(payload, encoding="utf-8")
                    node = self.context.fm.add_node(canvas.graph, node_path)
                    canvas.update_node_roi(node)
                    node.node_pos = canvas.mouse_to_canvas_coords()

        if imgui.begin_popup_context_window().opened:
            try:
                if menu_item("Reset"):
                    canvas.reset_controllers()
            finally:
                imgui.end_popup()

        canvas.draw_graph()
