# -*- coding: utf-8 -*-

from typing import Mapping

from cvp.config.sections.windows.flow import FlowSection
from cvp.config.sections.windows.manager.flow import FlowManagerSection
from cvp.context import Context
from cvp.types import override
from cvp.widgets.hoc.manager import ItemsProxy, ManagerWindow
from cvp.windows.managers.flow.info import FlowInfoTab


class FlowSectionsProxy(ItemsProxy[FlowSection]):
    def __init__(self, context: Context):
        self._context = context

    @override
    def __call__(self) -> Mapping[str, FlowSection]:
        return self._context.config.flow_sections


class FlowManagerWindow(ManagerWindow[FlowManagerSection, FlowSection]):
    def __init__(self, context: Context):
        super().__init__(
            context=context,
            section=context.config.flow_manager,
            proxy=FlowSectionsProxy(context),
            title="Flow Manager",
            closable=True,
            flags=None,
        )
        self.register(FlowInfoTab(context))
