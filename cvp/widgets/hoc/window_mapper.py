# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Optional

from cvp.widgets.hoc.window import Window


class WindowMapper(OrderedDict[str, Window]):
    def pop_window(self, key: str, *, no_destroy=False):
        if not self.__contains__(key):
            raise KeyError(f"Window '{key}' not exists")

        window = self.pop(key)
        if not no_destroy:
            window.do_destroy()

        return window

    def add_window(
        self,
        window: Window,
        key: Optional[str] = None,
        *,
        no_create=False,
    ) -> None:
        key = key if key else window.key
        assert isinstance(key, str)

        if self.__contains__(key):
            raise KeyError(f"Window '{key}' already exists")

        if not no_create:
            window.do_create()

        self.__setitem__(key, window)

    def add_windows(self, *windows: Window, no_create=False) -> None:
        for window in windows:
            self.add_window(window, no_create=no_create)

    def do_destroy(self):
        while self:
            key, win = self.popitem(last=False)
            win.do_destroy()

    def do_process(self):
        # [IMPORTANT]
        # Do not change the iteration count as elem may be removed in `do_process()`.
        # This method creates a shallow copy of the `list` object.
        for win in list(self.values()):
            win.do_process()
