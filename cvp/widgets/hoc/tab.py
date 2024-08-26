# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Optional

import imgui

from cvp.types.override import override
from cvp.widgets.hoc.widget import WidgetInterface


class TabItem(WidgetInterface):
    def __init__(self, label: str, opened: Optional[bool] = None, flags=0):
        self._label = label
        self._opened = opened
        self._flags = flags

    def begin(self):
        return imgui.begin_tab_item(self._label, self._opened, self._flags)

    def end(self) -> None:
        assert self
        imgui.end_tab_item()

    @override
    def do_process(self) -> None:
        if self.begin().selected:
            try:
                self.on_process()
            finally:
                self.end()

    @override
    def on_process(self) -> None:
        pass


class TabBar(WidgetInterface):
    _items: OrderedDict[str, TabItem]

    def __init__(self, identifier: str, flags=0):
        self._identifier = identifier
        self._flags = flags
        self._items = OrderedDict()

    def register(self, key: str, item: TabItem) -> None:
        self._items[key] = item

    def begin(self):
        return imgui.begin_tab_bar(self._identifier, self._flags)

    def end(self) -> None:
        assert self
        imgui.end_tab_bar()

    @override
    def do_process(self) -> None:
        if self.begin().opened:
            try:
                self.on_process()
            finally:
                self.end()

    @override
    def on_process(self) -> None:
        for item in self._items.values():
            item.do_process()
