# -*- coding: utf-8 -*-

from collections import deque
from dataclasses import dataclass
from typing import Deque, Final

import imgui

from cvp.config.sections.toast import ToastWindowConfig
from cvp.context.context import Context
from cvp.renderer.window.base import WindowBase
from cvp.types.override import override

TOAST_WINDOW_FLAGS: Final[int] = (
    imgui.WINDOW_NO_DECORATION
    | imgui.WINDOW_ALWAYS_AUTO_RESIZE
    | imgui.WINDOW_NO_SAVED_SETTINGS
    | imgui.WINDOW_NO_NAV
    | imgui.WINDOW_NO_MOVE
)


@dataclass
class ToastItem:
    message: str


class ToastWindow(WindowBase[ToastWindowConfig]):
    _items: Deque[ToastItem]

    def __init__(self, context: Context):
        super().__init__(
            context=context,
            window_config=context.config.toast_window,
            title="Toast",
            closable=False,
            flags=TOAST_WINDOW_FLAGS,
        )
        self._items = deque()

    def show_toast(self, item: ToastItem) -> None:
        self._items.append(item)
        self.opened = True

    def show_simple(self, message: str) -> None:
        self.show_toast(ToastItem(message))

    @override
    def on_before(self) -> None:
        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 15.0)

    @override
    def on_after(self) -> None:
        imgui.pop_style_var()

    @override
    def on_process(self) -> None:
        if not self._items:
            self.opened = False
            return

        item = self._items[0]
        imgui.text(item.message)

        if self.is_mouse_left_button_clicked():
            self._items.pop()
