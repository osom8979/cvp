# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Optional

from pygame.event import Event

from cvp.pgc.constants.event_type import KEY_EVENTS
from cvp.pgc.constants.keycode import Keycode
from cvp.pgc.constants.keymod import Keymod
from cvp.widgets.window import Window


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

    def as_windows(self):
        """
        [IMPORTANT]
        Do not change the iteration count as elem may be removed in `do_process()`.
        This method creates a shallow copy of the `list` object.
        """
        return list(self.values())

    def do_event(self, event: Event) -> bool:
        if event.type in KEY_EVENTS:
            event.key = Keycode(event.key)
            event.mod = Keymod(event.mod)

        for win in self.as_windows():
            consumed_event = win.do_event(event)
            if consumed_event:
                return True

        return False

    def do_destroy(self):
        while self:
            key, win = self.popitem(last=False)
            win.do_destroy()

    def do_process(self):
        for win in self.as_windows():
            win.do_process()
