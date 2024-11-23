# -*- coding: utf-8 -*-

from collections import deque
from dataclasses import dataclass
from time import time
from typing import Deque, Final, Optional, Union

import imgui

from cvp.config.sections.toast import ToastWindowConfig
from cvp.context.context import Context
from cvp.imgui.draw_list import get_foreground_draw_list
from cvp.logging.logging import (
    DEBUG,
    ERROR,
    INFO,
    NOTSET,
    WARNING,
    convert_level_number,
)
from cvp.renderer.window.base import WindowBase
from cvp.types.colors import RGB
from cvp.types.override import override

TOAST_WINDOW_FLAGS: Final[int] = (
    imgui.WINDOW_NO_DECORATION
    | imgui.WINDOW_ALWAYS_AUTO_RESIZE
    | imgui.WINDOW_NO_SAVED_SETTINGS
    | imgui.WINDOW_NO_MOVE
    | imgui.WINDOW_NO_NAV
    | imgui.WINDOW_UNSAVED_DOCUMENT
    | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS
    | imgui.WINDOW_NO_FOCUS_ON_APPEARING
    | imgui.WINDOW_NO_INPUTS
)


@dataclass
class ToastItem:
    message: str
    level: Optional[Union[str, int]] = None


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

    def reset_timer(self) -> None:
        self._begin = time()

    def pop_item(self) -> None:
        if not self._items:
            return
        self._items.pop()
        self.reset_timer()

    def show_toast(self, item: ToastItem) -> None:
        if not self._items:
            self.reset_timer()

        self._items.append(item)
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
            raise ValueError("Exceeded fadeout range")

    def get_level_color(self, level: Optional[Union[str, int]] = None) -> RGB:
        if level is None:
            return self.window_config.normal_color

        level = convert_level_number(level)
        assert isinstance(level, int)

        if WARNING < level <= ERROR:
            return self.window_config.error_color
        elif INFO < level <= WARNING:
            return self.window_config.warning_color
        elif DEBUG < level <= INFO:
            return self.window_config.normal_color
        elif NOTSET < level <= DEBUG:
            return self.window_config.success_color
        else:
            raise ValueError(f"Invalid level {level}")

    @override
    def on_before(self) -> None:
        imgui.set_next_window_bg_alpha(0)

    @override
    def on_process(self) -> None:
        if not self._items:
            self.opened = False
            return

        try:
            alpha = self.update_alpha(time())
        except ValueError:
            self.pop_item()
            return

        current_item = self._items[0]
        message = current_item.message
        level = current_item.level

        br, bg, bb = self._window_config.background_color
        assert isinstance(br, float)
        assert isinstance(bg, float)
        assert isinstance(bb, float)
        background_color = imgui.get_color_u32_rgba(br, bg, bb, alpha)

        fr, fg, fb = self.get_level_color(level)
        assert isinstance(fr, float)
        assert isinstance(fg, float)
        assert isinstance(fb, float)
        foreground_color = imgui.get_color_u32_rgba(fr, fg, fb, alpha)

        pivot_x = self.window_config.pivot_x
        pivot_y = self.window_config.pivot_y
        anchor_x = self.window_config.anchor_x
        anchor_y = self.window_config.anchor_y
        margin_x = self.window_config.margin_x
        margin_y = self.window_config.margin_y
        padding_x = self.window_config.padding_x
        padding_y = self.window_config.padding_y
        rounding = self.window_config.rounding

        viewport = imgui.get_main_viewport()
        work_pos = viewport.work_pos  # Use work area to avoid menu-bar/task-bar, if any
        work_size = viewport.work_size
        work_pos_x, work_pos_y = work_pos
        work_size_x, work_size_y = work_size

        canvas_pos_x = work_pos_x + margin_x
        canvas_pos_y = work_pos_y + margin_y
        canvas_size_x = work_size_x - margin_x * 2
        canvas_size_y = work_size_y - margin_y * 2

        text_width, text_height = imgui.calc_text_size(message)
        assert isinstance(text_width, float)
        assert isinstance(text_height, float)
        window_size_x = text_width + padding_x * 2
        window_size_y = text_height + padding_y * 2

        x1 = canvas_pos_x + (canvas_size_x * anchor_x) - (window_size_x * pivot_x)
        y1 = canvas_pos_y + (canvas_size_y * anchor_y) - (window_size_y * pivot_y)
        x2 = x1 + window_size_x
        y2 = y1 + window_size_y
        draw_list = get_foreground_draw_list()
        draw_list.add_rect_filled(x1, y1, x2, y2, background_color, rounding)

        text_x = x1 + padding_x
        text_y = y1 + padding_x
        draw_list.add_text(text_x, text_y, foreground_color, message)

        mx, my = imgui.get_mouse_pos()
        assert isinstance(mx, float)
        assert isinstance(my, float)

        hovering = x1 <= mx <= x2 and y1 <= my <= y2
        clicked = imgui.is_mouse_clicked(imgui.MOUSE_BUTTON_LEFT)

        if hovering and clicked:
            self.pop_item()
