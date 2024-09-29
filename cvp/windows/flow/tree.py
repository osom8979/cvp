# -*- coding: utf-8 -*-

from cvp.context import Context
from cvp.types import override
from cvp.widgets.widget import WidgetInterface


class Tree(WidgetInterface):
    def __init__(self, context: Context):
        self._context = context

    @override
    def on_process(self) -> None:
        pass
