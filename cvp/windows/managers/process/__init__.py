# -*- coding: utf-8 -*-

from typing import Mapping

from cvp.config.sections.windows.manager.process import ProcessManagerSection
from cvp.context import Context
from cvp.process.process import Process
from cvp.types import override
from cvp.widgets.hoc.manager_tab import ItemsProxy, ManagerTab
from cvp.windows.managers.process.info import ProcessInfoTab
from cvp.windows.managers.process.stream import ProcessStreamTab


class ProcessesProxy(ItemsProxy[Process]):
    def __init__(self, context: Context):
        self._context = context

    @override
    def __call__(self) -> Mapping[str, Process]:
        return self._context.pm.processes


class ProcessManagerWindow(ManagerTab[ProcessManagerSection, Process]):
    def __init__(self, context: Context):
        super().__init__(
            context=context,
            section=context.config.process_manager,
            proxy=ProcessesProxy(context),
            title="Process Manager",
            closable=True,
            flags=None,
        )
        self.register(ProcessInfoTab(context))
        self.register(ProcessStreamTab.from_stdout(context))
        self.register(ProcessStreamTab.from_stderr(context))
