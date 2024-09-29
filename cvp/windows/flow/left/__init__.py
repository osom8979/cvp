# -*- coding: utf-8 -*-

from cvp.context import Context
from cvp.widgets.tab import TabBar
from cvp.windows.flow.left.catalogs import CatalogsTab
from cvp.windows.flow.left.graphs import GraphsTab


class FlowLeftTabs(TabBar):
    def __init__(self, context: Context):
        super().__init__(
            context=context,
            identifier="## FlowLeftTabs",
            flags=0,
        )
        self.register(GraphsTab(context))
        self.register(CatalogsTab(context))
