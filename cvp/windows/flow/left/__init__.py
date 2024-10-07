# -*- coding: utf-8 -*-

from cvp.context import Context
from cvp.flow.templates.graph import FlowGraph
from cvp.widgets.tab import TabBar
from cvp.windows.flow.left.graph import GraphTab
from cvp.windows.flow.left.tree import TreeTab


class FlowLeftTabs(TabBar[FlowGraph]):
    def __init__(self, context: Context):
        super().__init__(
            context=context,
            identifier="## FlowLeftTabs",
            flags=0,
        )
        self.register(GraphTab(context))
        self.register(TreeTab(context))
