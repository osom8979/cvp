# -*- coding: utf-8 -*-

from cvp.context.context import Context
from cvp.flow.datas.graph import Graph
from cvp.imgui.fonts.mapper import FontMapper
from cvp.widgets.tab import TabBar
from cvp.windows.flow.bottom.history import HistoryTab
from cvp.windows.flow.bottom.logs import LogsTab
from cvp.windows.flow.cursor import FlowCursor


class FlowBottomTabs(TabBar[Graph]):
    def __init__(self, context: Context, fonts: FontMapper, cursor: FlowCursor):
        super().__init__(
            context=context,
            identifier="## FlowBottomTabs",
            flags=0,
        )
        self.register(LogsTab(context, fonts, cursor))
        self.register(HistoryTab(context, fonts, cursor))
