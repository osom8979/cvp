# -*- coding: utf-8 -*-

from cvp.context import Context
from cvp.widgets.tab import TabBar
from cvp.windows.flow.bottom.logs import LogsTab


class FlowBottomTabs(TabBar):
    def __init__(self, context: Context):
        super().__init__(
            context=context,
            identifier="## FlowBottomTabs",
            flags=0,
        )
        self.register(LogsTab(context))
