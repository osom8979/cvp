# -*- coding: utf-8 -*-

from cvp.context import Context
from cvp.process.process import Process
from cvp.widgets.hoc.tab import TabBar
from cvp.windows.processes.tabs.info import ProcessInfoTab
from cvp.windows.processes.tabs.stream import ProcessStreamTab


class ProcessTabs(TabBar[Process]):
    def __init__(self, context: Context):
        super().__init__(context)
        self.register(ProcessInfoTab(context))
        self.register(ProcessStreamTab.from_stdout(context))
        self.register(ProcessStreamTab.from_stderr(context))
