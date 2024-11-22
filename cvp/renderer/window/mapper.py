# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import List, Optional, Sequence

from pygame.event import Event

from cvp.itertools.find_index import NOT_FOUND_INDEX, find_index
from cvp.msgs.msg import Msg
from cvp.pygame.constants.event_type import KEY_EVENTS
from cvp.pygame.constants.keycode import Keycode
from cvp.pygame.constants.keymod import Keymod
from cvp.renderer.window.base import WindowBase


class WindowMapper(OrderedDict[str, WindowBase]):
    def set_removable(self, uuid: str) -> None:
        self.__getitem__(uuid).set_removable()

    def add_window(
        self,
        window: WindowBase,
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

    @staticmethod
    def reorder_windows(
        windows: Sequence[WindowBase],
        begin_order: List[str],
    ) -> List[WindowBase]:
        remain_windows = list(windows)
        ordered_windows = list()
        for key in begin_order:
            index = find_index(remain_windows, lambda w: w.key == key)
            if index != NOT_FOUND_INDEX:
                ordered_windows.append(remain_windows.pop(index))
        ordered_windows.extend(remain_windows)
        ordered_windows.reverse()
        return ordered_windows

    def add_windows(
        self,
        *windows: WindowBase,
        no_create=False,
        begin_order: Optional[List[str]] = None,
    ) -> None:
        if begin_order:
            windows = tuple(self.reorder_windows(windows, begin_order))
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

    def do_msg(self, msg: Msg) -> bool:
        for win in self.as_windows():
            consumed_msg = win.do_msg(msg)
            if consumed_msg:
                return True

        return False

    def do_destroy(self):
        while self:
            key, win = self.popitem(last=False)
            win.do_destroy()

    def do_process(self):
        for win in self.as_windows():
            win.do_process()

    def do_next(self):
        for key in list(key for key, win in self.items() if win.removable):
            self.pop(key).do_destroy()
