# -*- coding: utf-8 -*-

from cvp.context.context import Context
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.types.override import override
from cvp.widgets.tab import TabItem


class PropsTab(TabItem[str]):
    def __init__(self, context: Context):
        super().__init__(context, "Props")

    @override
    def on_item(self, item: str) -> None:
        if self.context.fm.opened:
            if item:
                self.on_item_cursor(item)
            else:
                self.on_graph_cursor()
        else:
            self.on_none()

    @override
    def on_none(self) -> None:
        pass

    def on_graph_cursor(self) -> None:
        graph = self.context.fm.current_graph
        assert graph is not None

        input_text_disabled("UUID", graph.uuid)

    def on_item_cursor(self, item: str) -> None:
        graph = self.context.fm.current_graph
        assert graph is not None

        input_text_disabled("Key", item)
