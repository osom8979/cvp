# -*- coding: utf-8 -*-

from cvp.context import Context
from cvp.widgets.tab import TabBar
from cvp.windows.flow.right.props import PropsTab


class FlowRightTabs(TabBar[str]):
    def __init__(self, context: Context):
        super().__init__(
            context=context,
            identifier="## FlowRightTabs",
            flags=0,
        )
        self.register(PropsTab(context))
