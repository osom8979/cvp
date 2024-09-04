# -*- coding: utf-8 -*-

from cvp.process.process import Process
from cvp.widgets.hoc.tab import TabBar
from cvp.windows.processes.tabs.info import ProcessInfoTab
from cvp.windows.processes.tabs.stream import ProcessStreamTab


class ProcessTabs(TabBar[Process]):
    def __init__(self):
        super().__init__()
        self.register(ProcessInfoTab())
        self.register(ProcessStreamTab.from_stdout())
        self.register(ProcessStreamTab.from_stderr())
