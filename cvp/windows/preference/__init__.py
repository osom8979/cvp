# -*- coding: utf-8 -*-

import imgui

from cvp.config.config import Config
from cvp.config.sections.preference import PreferenceSection
from cvp.types.override import override
from cvp.variables import MIN_SIDEBAR_WIDTH
from cvp.widgets.hoc.window import Window


class PreferenceWindow(Window[PreferenceSection]):
    def __init__(self, config: Config):
        super().__init__(config.preference, title="Preference", closable=True)
        self._config = config
        self._min_sidebar_width = MIN_SIDEBAR_WIDTH
        self._menus = ("Appearance", "FFmpeg")

    @property
    def sidebar_width(self) -> int:
        return self.section.sidebar_width

    @sidebar_width.setter
    def sidebar_width(self, value: int) -> None:
        self.section.sidebar_width = value

    @property
    def menu_index(self) -> int:
        return self.section.menu_index

    @menu_index.setter
    def menu_index(self, value: int) -> None:
        self.section.menu_index = value

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

    @override
    def on_process(self) -> None:
        # noinspection PyArgumentList
        imgui.begin_child("## Sidebar", self.sidebar_width, 0, border=True)
        try:
            imgui.text("Sidebar Menu")

            content_width = imgui.get_content_region_available_width()
            imgui.set_next_item_width(content_width)
            self.drag_sidebar_width()

            menus = imgui.begin_list_box("## SideList", width=-1, height=-1)
            if menus.opened:
                for i, menu in enumerate(self._menus):
                    if imgui.selectable(menu, i == self.menu_index)[1]:
                        self.menu_index = i
                imgui.end_list_box()
        finally:
            imgui.end_child()
