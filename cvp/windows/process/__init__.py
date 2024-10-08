# -*- coding: utf-8 -*-

from typing import Mapping

from cvp.config.sections.process import ProcessConfig
from cvp.context.context import Context
from cvp.process.process import Process
from cvp.types import override
from cvp.widgets.manager_tab import ManagerTab
from cvp.windows.process.info import ProcessInfoTab
from cvp.windows.process.stream import ProcessStreamTab


class ProcessManager(ManagerTab[ProcessConfig, Process]):
    def __init__(self, context: Context):
        super().__init__(
            context=context,
            section=context.config.process,
            title="Process Manager",
            closable=True,
            flags=None,
        )
        self.register(ProcessInfoTab(context))
        self.register(ProcessStreamTab.from_stdout(context))
        self.register(ProcessStreamTab.from_stderr(context))

    @override
    def get_menus(self) -> Mapping[str, Process]:
        return self._context.pm.processes
