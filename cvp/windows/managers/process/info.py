# -*- coding: utf-8 -*-

import imgui

from cvp.context import Context
from cvp.process.process import Process
from cvp.types import override
from cvp.widgets import button_ex, input_text_disabled
from cvp.widgets.hoc.tab import TabItem


class ProcessInfoTab(TabItem[Process]):
    def __init__(self, context: Context):
        super().__init__(context, "Info")

    @override
    def on_item(self, item: Process) -> None:
        imgui.text("Name:")
        input_text_disabled("## Name", item.name)

        imgui.text("PID:")
        input_text_disabled("## PID", str(item.pid))

        imgui.text("Status:")
        input_text_disabled("## Status", str(item.status()))

        imgui.separator()

        key = item.name
        spawnable = self.context.pm.spawnable(key)
        stoppable = self.context.pm.stoppable(key)
        removable = self.context.pm.removable(key)

        if button_ex("Spawn", disabled=not spawnable):
            pass
        imgui.same_line()
        if button_ex("Stop", disabled=not stoppable):
            self.context.pm.interrupt(key)
        imgui.same_line()
        if button_ex("Remove", disabled=not removable):
            self.context.pm.pop(key)
