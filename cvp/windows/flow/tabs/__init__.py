# -*- coding: utf-8 -*-

from cvp.context import Context
from cvp.widgets.hoc.tab import TabBar


class Tabs(TabBar):
    def __init__(self, context: Context):
        super().__init__(
            context=context,
            identifier="## FlowTabs",
            flags=0,
        )
