# -*- coding: utf-8 -*-

import imgui

from cvp.process.manager import ProcessManager
from cvp.process.process import Process
from cvp.types import override
from cvp.widgets import button_ex, input_text_disabled
from cvp.widgets.hoc.tab import TabItem


class ProcessInfoTab(TabItem[Process]):
    def __init__(self, pm: ProcessManager):
        super().__init__("Info")
        self._pm = pm

    @override
    def on_context(self, context: Process) -> None:
        imgui.text("Name:")
        input_text_disabled("## Name", context.name)

        imgui.text("PID:")
        input_text_disabled("## PID", str(context.pid))

        imgui.text("Status:")
        input_text_disabled("## Status", str(context.status()))

        imgui.separator()

        key = context.name
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
