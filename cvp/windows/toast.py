# -*- coding: utf-8 -*-

from collections import deque
from dataclasses import dataclass
from time import time
from typing import Deque, Final, Tuple

import imgui

from cvp.config.sections.toast import ToastWindowConfig
from cvp.context.context import Context
from cvp.renderer.window.base import WindowBase
from cvp.types.override import override

TOAST_WINDOW_FLAGS: Final[int] = (
    imgui.WINDOW_NO_DECORATION
    | imgui.WINDOW_ALWAYS_AUTO_RESIZE
    | imgui.WINDOW_NO_SAVED_SETTINGS
    | imgui.WINDOW_NO_MOVE
    | imgui.WINDOW_NO_NAV
    | imgui.WINDOW_UNSAVED_DOCUMENT
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
        self._begin = time()

    def show_toast(self, item: ToastItem) -> None:
        self._items.append(item)
        self._begin = time()
        self.opened = True

    def show_simple(self, message: str) -> None:
        self.show_toast(ToastItem(message))

    @property
    def fadein(self):
        return self.window_config.fadein

    @property
    def fadeout(self):
        return self.window_config.fadeout

    @property
    def waiting(self):
        return self.window_config.waiting

    def update_alpha(self, now: float) -> float:
        elapsed = now - self._begin
        if elapsed <= self.fadein:
            return elapsed / self.fadein
        elif elapsed <= self.fadein + self.waiting:
            return 1.0
        elif elapsed <= self.fadein + self.waiting + self.fadeout:
            return 1.0 - (elapsed - self.fadein - self.waiting) / self.fadeout
        else:
            return -1.0

    @property
    def window_position(self) -> Tuple[float, float]:
        viewport = imgui.get_main_viewport()
        work_pos = viewport.work_pos  # Use work area to avoid menu-bar/task-bar, if any
        work_size = viewport.work_size
        work_pos_x, work_pos_y = work_pos
        work_size_x, work_size_y = work_size

        margin_x = self.window_config.margin_x
        margin_y = self.window_config.margin_y

        work_pos_x += margin_x
        work_pos_y += margin_y
        work_size_x -= margin_x * 2
        work_size_y -= margin_y * 2

        anchor_x = self.window_config.anchor_x
        anchor_y = self.window_config.anchor_y

        x = work_pos_x + work_size_x * anchor_x
        y = work_pos_y + work_size_y * anchor_y
        return x, y

    @override
    def on_before(self) -> None:
        rounding = self.window_config.rounding
        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, rounding)

        padding_x = self.window_config.padding_x
        padding_y = self.window_config.padding_y
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (padding_x, padding_y))

        background_color = self.window_config.background_color
        imgui.push_style_color(imgui.COLOR_CHILD_BACKGROUND, *background_color)

        pos_x, pos_y = self.window_position
        pivot_x = self.window_config.pivot_x
        pivot_y = self.window_config.pivot_y
        imgui.set_next_window_position(pos_x, pos_y, imgui.ALWAYS, pivot_x, pivot_y)

        alpha = self.update_alpha(time())
        if 0 <= alpha:
            imgui.set_next_window_bg_alpha(alpha)
        else:
            assert alpha < 0
            if self._items:
                self._items.pop()

    @override
    def on_after(self) -> None:
        imgui.pop_style_color()
        imgui.pop_style_var(2)

    @override
    def on_process(self) -> None:
        if not self._items:
            self.opened = False
            return

        item = self._items[0]
        imgui.text(item.message)

        if self.is_mouse_left_button_clicked():
            self._items.pop()
