# -*- coding: utf-8 -*-

from typing import List

import imgui

from cvp.config.config import Config
from cvp.config.sections.windows.preference import PreferenceSection
from cvp.types import override
from cvp.variables import MIN_SIDEBAR_WIDTH
from cvp.widgets import begin_child, end_child, footer_height_to_reserve, text_centered
from cvp.widgets.hoc.widget import WidgetInterface
from cvp.widgets.hoc.window import Window
from cvp.windows.preference.appearance import AppearancePreference
from cvp.windows.preference.ffmpeg import FFmpegPreference
from cvp.windows.preference.logging import LoggingPreference


class PreferenceWindow(Window[PreferenceSection]):
    _menus: List[WidgetInterface]

    def __init__(self, config: Config):
        super().__init__(config.preference, title="Preference", closable=True)
        self._config = config
        self._min_sidebar_width = MIN_SIDEBAR_WIDTH
        self._menus = [
            AppearancePreference(),
            FFmpegPreference(config.ffmpeg),
            LoggingPreference(config.logging),
        ]

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
        if begin_child("## Sidebar", self.sidebar_width, border=True).visible:
            try:
                content_width = imgui.get_content_region_available_width()
                imgui.set_next_item_width(content_width)
                self.drag_sidebar_width()

                imgui.separator()

                if imgui.begin_list_box("## SideList", width=-1, height=-1).opened:
                    for i, menu in enumerate(self._menus):
                        if imgui.selectable(str(menu), i == self.menu_index)[1]:
                            self.menu_index = i
                    imgui.end_list_box()
            finally:
                end_child()

        imgui.same_line()

        if begin_child("## Main", -1, -footer_height_to_reserve()).visible:
            try:
                if 0 <= self.menu_index < len(self._menus):
                    menu = self._menus[self.menu_index]
                    imgui.text(str(menu))
                    imgui.separator()
                    menu.on_process()
                else:
                    text_centered("Please select a menu item")
            finally:
                end_child()
