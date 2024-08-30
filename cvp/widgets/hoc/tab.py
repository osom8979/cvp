# -*- coding: utf-8 -*-

from abc import abstractmethod
from collections import OrderedDict
from typing import Generic, Optional, TypeVar

import imgui

from cvp.types.override import override
from cvp.widgets.hoc.widget import WidgetInterface

ContextT = TypeVar("ContextT")


class TabItem(Generic[ContextT], WidgetInterface):
    _context: Optional[ContextT]

    def __init__(self, label: str, opened: Optional[bool] = None, flags=0):
        self._label = label
        self._opened = opened
        self._flags = flags
        self._context = None

    @property
    def label(self):
        return self._label

    @property
    def context(self):
        return self._context

    def begin(self):
        return imgui.begin_tab_item(self._label, self._opened, self._flags)

    def end(self) -> None:
        assert self
        imgui.end_tab_item()

    def do_process(self, context: Optional[ContextT] = None) -> None:
        if not self.begin().selected:
            return

        self._context = context
        try:
            self.on_process()
        finally:
            self._context = None
            self.end()

    @override
    def on_process(self) -> None:
        if self._context is not None:
            self.on_context(self._context)

    @abstractmethod
    def on_context(self, context: ContextT) -> None:
        pass


class TabBar(Generic[ContextT], WidgetInterface):
    _items: OrderedDict[str, TabItem]
    _context: Optional[ContextT]

    def __init__(self, identifier: Optional[str] = None, flags=0):
        self._identifier = identifier if identifier else type(self).__name__
        self._flags = flags
        self._items = OrderedDict()
        self._context = None

    @property
    def identifier(self):
        return self._identifier

    @property
    def context(self):
        return self._context

    def register(self, item: TabItem) -> None:
        self._items[item.label] = item

    def begin(self):
        return imgui.begin_tab_bar(self._identifier, self._flags)

    def end(self) -> None:
        assert self
        imgui.end_tab_bar()

    def do_process(self, context: Optional[ContextT] = None) -> None:
        if not self.begin().opened:
            return

        self._context = context
        try:
            self.on_process()
        finally:
            self._context = None
            self.end()

    @override
    def on_process(self) -> None:
        for item in self._items.values():
            item.do_process(self._context)
