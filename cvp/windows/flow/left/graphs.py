# -*- coding: utf-8 -*-

from typing import Final

import imgui

from cvp.context.context import Context
from cvp.flow.datas import Graph
from cvp.types import override
from cvp.widgets.tab import TabItem

DOUBLE_CLICK: Final[int] = imgui.SELECTABLE_ALLOW_DOUBLE_CLICK


class GraphsTab(TabItem[Graph]):
    def __init__(self, context: Context):
        super().__init__(context, "Graphs")

    @override
    def on_process(self) -> None:
        current_uuid = self._item.uuid if self._item is not None else str()
        for uuid, graph in self.context.fm.items():
            imgui.bullet()
            imgui.same_line()

            selected = current_uuid == uuid
            if imgui.selectable(graph.name, selected, DOUBLE_CLICK):
                if imgui.is_mouse_double_clicked(0):
                    self.context.fm.open_graph(uuid)