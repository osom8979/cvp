# -*- coding: utf-8 -*-

import imgui

from cvp.config.config import Config
from cvp.variables import MIN_SIDEBAR_WIDTH, MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH


class ManagerWindow:
    def __init__(self, config: Config):
        self._config = config
        self._flags = 0
        self._min_width = MIN_WINDOW_WIDTH
        self._min_height = MIN_WINDOW_HEIGHT
        self._min_sidebar_width = MIN_SIDEBAR_WIDTH
        self._items = ("Video1", "Video2")

    @property
    def opened(self) -> bool:
        return self._config.manager.opened

    @opened.setter
    def opened(self, value: bool) -> None:
        self._config.manager.opened = value

    @property
    def sidebar_width(self) -> int:
        return self._config.manager.sidebar_width

    @sidebar_width.setter
    def sidebar_width(self, value: int) -> None:
        self._config.manager.sidebar_width = value

    @property
    def item_index(self) -> int:
        return self._config.manager.item_index

    @item_index.setter
    def item_index(self, value: int) -> None:
        self._config.manager.item_index = value

    def process(self) -> None:
        self._process_window()

    def _process_window(self) -> None:
        if not self.opened:
            return

        expanded, opened = imgui.begin("Manager", True, self._flags)
        try:
            if not opened:
                self.opened = False
                return

            if not expanded:
                return

            self._main()
        finally:
            imgui.end()

    def drag_sidebar_width(self):
        sidebar_width = imgui.drag_int(
            "## SideWidth",
            self.sidebar_width,
            1.0,
            self._min_sidebar_width,
            0,
            "Sidebar Width %d",
        )[1]
        if sidebar_width < self._min_sidebar_width:
            sidebar_width = self._min_sidebar_width
        self.sidebar_width = sidebar_width

    def _main(self) -> None:
        if imgui.is_window_appearing():
            imgui.set_window_size(self._min_width, self._min_height)

        # noinspection PyArgumentList
        imgui.begin_child("## Sidebar", self.sidebar_width, 0, border=True)
        try:
            imgui.text("Videos")

            content_width = imgui.get_content_region_available_width()
            imgui.set_next_item_width(content_width)
            self.drag_sidebar_width()

            menus = imgui.begin_list_box("## SideList", width=-1, height=-1)
            if menus.opened:
                for i, item in enumerate(self._items):
                    if imgui.selectable(item, i == self.item_index)[1]:
                        self.item_index = i
                imgui.end_list_box()
        finally:
            imgui.end_child()
