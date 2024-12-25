# -*- coding: utf-8 -*-

from cvp.context.context import Context
from cvp.flow.datas.graph import Graph
from cvp.widgets.tab import TabBar
from cvp.windows.flow.bottom.history import HistoryTab
from cvp.windows.flow.bottom.logs import LogsTab


class FlowBottomTabs(TabBar[Graph]):
    def __init__(self, context: Context):
        super().__init__(
            context=context,
            identifier="## FlowBottomTabs",
            flags=0,
        )
        self.register(LogsTab(context))
        self.register(HistoryTab(context))
