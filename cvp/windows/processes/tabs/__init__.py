# -*- coding: utf-8 -*-

from cvp.process.manager import ProcessManager
from cvp.process.process import Process
from cvp.widgets.hoc.tab import TabBar
from cvp.windows.processes.tabs.info import ProcessInfoTab
from cvp.windows.processes.tabs.stream import ProcessStreamTab


class ProcessTabs(TabBar[Process]):
    def __init__(self, pm: ProcessManager):
        super().__init__()
        self.register(ProcessInfoTab(pm))
        self.register(ProcessStreamTab.from_stdout())
        self.register(ProcessStreamTab.from_stderr())
