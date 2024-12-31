# -*- coding: utf-8 -*-

import imgui

from cvp.context.context import Context
from cvp.flow.datas.graph import Graph
from cvp.imgui.fonts.mapper import FontMapper
from cvp.types.override import override
from cvp.widgets.tab import TabItem
from cvp.windows.flow.cursor import FlowCursor


class GraphsTab(TabItem[Graph]):
    def __init__(self, context: Context, fonts: FontMapper, cursor: FlowCursor):
        super().__init__(context, "Graphs")
        self._fonts = fonts
        self._cursor = cursor

    @override
    def on_process(self) -> None:
        current_uuid = self._item.uuid if self._item is not None else str()
        for uuid, graph in self.context.fm.items():
            imgui.bullet()
            imgui.same_line()

            label = f"{graph.name}##{uuid}"
            selected = uuid == current_uuid
            flags = imgui.SELECTABLE_ALLOW_DOUBLE_CLICK

            if imgui.selectable(label, selected, flags)[0]:
                if imgui.is_mouse_double_clicked(0):
                    self._cursor.open(graph)
