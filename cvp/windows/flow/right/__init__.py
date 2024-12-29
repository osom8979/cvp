# -*- coding: utf-8 -*-

from cvp.context.context import Context
from cvp.flow.datas.graph import Graph
from cvp.imgui.fonts.mapper import FontMapper
from cvp.widgets.tab import TabBar
from cvp.windows.flow.right.props import PropsTab


class FlowRightTabs(TabBar[Graph]):
    def __init__(self, context: Context, fonts: FontMapper):
        super().__init__(
            context=context,
            identifier="## FlowRightTabs",
            flags=0,
        )
        self.register(PropsTab(context, fonts))
