# -*- coding: utf-8 -*-

import imgui

from cvp.config.sections.windows.processes import ProcessesSection
from cvp.types import override
from cvp.variables import MIN_SIDEBAR_WIDTH
from cvp.widgets import begin_child, end_child, text_centered
from cvp.widgets.hoc.window import Window
from cvp.windows.processes.tabs import ProcessTabs


class ProcessesWindow(Window[ProcessesSection]):
    def __init__(self):
        super().__init__(
            self.propagated_context().config.processes,
            title="Processes",
            closable=True,
            flags=None,
        )

        self._min_sidebar_width = MIN_SIDEBAR_WIDTH
        self._tabs = ProcessTabs()

    @property
    def sidebar_width(self) -> int:
        return self.section.sidebar_width

    @sidebar_width.setter
    def sidebar_width(self, value: int) -> None:
        self.section.sidebar_width = value

    @property
    def selected(self) -> str:
        return self.section.selected

    @selected.setter
    def selected(self, value: str) -> None:
        self.section.selected = value

    def drag_sidebar_width(self) -> None:
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
                    for key, section in self.context.pm.items():
                        if imgui.selectable(section.name, key == self.selected)[1]:
                            self.selected = key
                    imgui.end_list_box()
            finally:
                end_child()

        imgui.same_line()

        if begin_child("## Main", -1, -1).visible:
            try:
                proc = self.context.pm.get(self.selected)
                if proc is not None:
                    self._tabs.do_process(proc)
                else:
                    text_centered("Please select a process item")
            finally:
                end_child()
