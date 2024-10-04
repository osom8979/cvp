# -*- coding: utf-8 -*-

import imgui

from cvp.context import Context
from cvp.types import override
from cvp.widgets.widget import WidgetInterface
from cvp.windows.flow.drag_type import DRAG_NODE_TYPE


class Catalogs(WidgetInterface):
    def __init__(self, context: Context):
        self._context = context
        self._cat1 = True
        self._cat2 = True

    def update_catalog(self):
        categories = list()
        for key, node in self._context.fm.catalog.items():
            pass
        return categories

    @override
    def on_process(self) -> None:
        imgui.text("Catalogs:")

        expanded, visible = imgui.collapsing_header("Cat1", self._cat1)
        if expanded:
            imgui.button("Node")

            with imgui.begin_drag_drop_source() as drag_drop_src:
                if drag_drop_src.dragging:
                    imgui.set_drag_drop_payload(DRAG_NODE_TYPE, b"payload")
                    imgui.button("Dragged Node")

        expanded, visible = imgui.collapsing_header("Cat2", self._cat2)
        if expanded:
            imgui.text("Now you see me!")
