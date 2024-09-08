# -*- coding: utf-8 -*-

from typing import Mapping

from cvp.config.sections.windows.flow import FlowSection
from cvp.config.sections.windows.manager.flow import FlowManagerSection
from cvp.context import Context
from cvp.types import override
from cvp.widgets.hoc.manager_tab import ManagerTab
from cvp.windows.managers.flow.info import FlowInfoTab


class FlowManagerWindow(ManagerTab[FlowManagerSection, FlowSection]):
    def __init__(self, context: Context):
        super().__init__(
            context=context,
            section=context.config.flow_manager,
            title="Flow Manager",
            closable=True,
            flags=None,
        )
        self.register(FlowInfoTab(context))

    @override
    def get_menus(self) -> Mapping[str, FlowSection]:
        return self._context.config.flow_sections
