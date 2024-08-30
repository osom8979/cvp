# -*- coding: utf-8 -*-

import imgui

from cvp.config.config import Config
from cvp.config.sections.processes import ProcessesSection
from cvp.process.manager import ProcessManager
from cvp.process.process import Process
from cvp.types.override import override
from cvp.variables import MIN_SIDEBAR_WIDTH
from cvp.widgets import (
    begin_child,
    button_ex,
    end_child,
    footer_height_to_reserve,
    input_text_disabled,
    text_centered,
)
from cvp.widgets.hoc.window import Window


class ProcessesWindow(Window[ProcessesSection]):
    def __init__(self, pm: ProcessManager, config: Config):
        super().__init__(config.manager, title="Processes", closable=True)
        self._pm = pm
        self._min_sidebar_width = MIN_SIDEBAR_WIDTH

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
                    for key, section in self._pm.items():
                        if imgui.selectable(section.name, key == self.selected)[1]:
                            self.selected = key
                    imgui.end_list_box()
            finally:
                end_child()

        imgui.same_line()

        if begin_child("## Main", -1, -footer_height_to_reserve()).visible:
            try:
                proc = self._pm.get(self.selected, None)
                if proc is not None:
                    self._process_tab_bar(proc)
                else:
                    text_centered("Please select a process item")
            finally:
                end_child()

    def _process_tab_bar(self, proc: Process) -> None:
        if not imgui.begin_tab_bar("Process Tabs"):
            return

        try:
            self._basic_tab(proc)
        finally:
            imgui.end_tab_bar()

    def _basic_tab(self, proc: Process) -> None:
        if not imgui.begin_tab_item("Basic").selected:
            return

        try:
            imgui.text("Name:")
            input_text_disabled("## Name", proc.name)

            imgui.text("PID:")
            input_text_disabled("## PID", str(proc.pid))

            imgui.text("Status:")
            input_text_disabled("## Status", str(proc.status()))

            imgui.separator()

            key = proc.name
            spawnable = self._pm.spawnable(key)
            stoppable = self._pm.stoppable(key)
            removable = self._pm.removable(key)

            if button_ex("Spawn", disabled=not spawnable):
                pass
            imgui.same_line()
            if button_ex("Stop", disabled=not stoppable):
                self._pm.interrupt(key)
            imgui.same_line()
            if button_ex("Remove", disabled=not removable):
                self._pm.pop(key)
        finally:
            imgui.end_tab_item()
