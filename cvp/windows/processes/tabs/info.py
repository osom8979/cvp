# -*- coding: utf-8 -*-

from typing import Optional
from weakref import ref

import imgui

from cvp.process.manager import ProcessManager
from cvp.process.process import Process
from cvp.types.override import override
from cvp.widgets import button_ex, input_text_disabled, text_centered
from cvp.widgets.hoc.tab import TabItem


class ProcessInfoTab(TabItem[Process]):
    def __init__(self, pm: ProcessManager):
        super().__init__("Info")
        self._pm = ref(pm)

    @property
    def pm(self) -> Optional[ProcessManager]:
        return self._pm()

    @override
    def on_context(self, context: Process) -> None:
        pm = self.pm
        if pm is None:
            text_centered("ProcessManager reference is dead")
            return

        imgui.text("Name:")
        input_text_disabled("## Name", context.name)

        imgui.text("PID:")
        input_text_disabled("## PID", str(context.pid))

        imgui.text("Status:")
        input_text_disabled("## Status", str(context.status()))

        imgui.separator()

        key = context.name
        spawnable = pm.spawnable(key)
        stoppable = pm.stoppable(key)
        removable = pm.removable(key)

        if button_ex("Spawn", disabled=not spawnable):
            pass
        imgui.same_line()
        if button_ex("Stop", disabled=not stoppable):
            pm.interrupt(key)
        imgui.same_line()
        if button_ex("Remove", disabled=not removable):
            pm.pop(key)
