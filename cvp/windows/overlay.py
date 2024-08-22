# -*- coding: utf-8 -*-

from math import floor
from typing import Final, Tuple

import imgui
from overrides import override

from cvp.config.sections.overlay import OverlaySection
from cvp.system.usage import SystemUsage
from cvp.widgets import menu_item_ex
from cvp.widgets.hoc.window import Window

OVERLAY_WINDOW_FLAGS: Final[int] = (
    imgui.WINDOW_NO_DECORATION
    | imgui.WINDOW_ALWAYS_AUTO_RESIZE
    | imgui.WINDOW_NO_SAVED_SETTINGS
    | imgui.WINDOW_NO_NAV
    | imgui.WINDOW_NO_MOVE
)


class OverlayWindow(Window[OverlaySection]):
    def __init__(self, section: OverlaySection):
        super().__init__(section, title="Overlay Window", flags=OVERLAY_WINDOW_FLAGS)

        self._normal_color = 0.0, 1.0, 0.0
        self._warning_color = 1.0, 1.0, 0.0
        self._error_color = 1.0, 0.0, 0.0

        self._usage = SystemUsage(interval=1.0)

    @property
    def is_left_side(self):
        return self.section.is_left_side

    @property
    def is_top_side(self):
        return self.section.is_top_side

    @property
    def window_position(self) -> Tuple[float, float]:
        viewport = imgui.get_main_viewport()
        work_pos = viewport.work_pos  # Use work area to avoid menu-bar/task-bar, if any
        work_size = viewport.work_size
        work_pos_x, work_pos_y = work_pos
        work_size_x, work_size_y = work_size
        padding = self.section.padding
        x = work_pos_x + (padding if self.is_left_side else work_size_x - padding)
        y = work_pos_y + (padding if self.is_top_side else work_size_y - padding)
        return x, y

    @property
    def window_pivot(self) -> Tuple[float, float]:
        x = 0.0 if self.is_left_side else 1.0
        y = 0.0 if self.is_top_side else 1.0
        return x, y

    def get_framerate_color(self, framerate: float) -> Tuple[float, float, float]:
        if framerate >= self.section.fps_warning_threshold:
            return self._normal_color
        elif framerate >= self.section.fps_error_threshold:
            return self._warning_color
        else:
            return self._error_color

    @override
    def on_process(self) -> None:
        framerate = imgui.get_io().framerate
        framerate_color = self.get_framerate_color(framerate)
        imgui.text_colored(f"FPS: {floor(framerate)}", *framerate_color)

        imgui.separator()

        usage = self._usage.update_interval()
        imgui.text(f"CPU: {usage.cpu:3.1f}%")
        imgui.text(f"VMEM: {usage.vmem:3.1f}%")

        imgui.separator()

        mouse_pos = imgui.get_mouse_pos()
        imgui.text(f"Mouse: {floor(mouse_pos.x)}, {floor(mouse_pos.y)}")

        if imgui.begin_popup_context_window():
            if menu_item_ex("Top-Left", self.section.is_top_left):
                self.section.set_top_left()
            if menu_item_ex("Top-Right", self.section.is_top_right):
                self.section.set_top_right()
            if menu_item_ex("Bottom-Left", self.section.is_bottom_left):
                self.section.set_bottom_left()
            if menu_item_ex("Bottom-Right", self.section.is_bottom_right):
                self.section.set_bottom_right()
            imgui.separator()
            if menu_item_ex("Close"):
                self.opened = False
            imgui.end_popup()

    @override
    def begin(self) -> Tuple[bool, bool]:
        pos_x, pos_y = self.window_position
        pivot_x, pivot_y = self.window_pivot
        imgui.set_next_window_position(pos_x, pos_y, imgui.ALWAYS, pivot_x, pivot_y)
        imgui.set_next_window_bg_alpha(self.section.alpha)
        return super().begin()
