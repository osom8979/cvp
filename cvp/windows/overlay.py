# -*- coding: utf-8 -*-

from math import floor
from typing import Final, Sequence, Tuple

import imgui

from cvp.config.sections.windows.overlay import OverlaySection
from cvp.context import Context
from cvp.gui import begin_popup_context_window, end_popup_context_window, menu_item_ex
from cvp.system.usage import SystemUsage
from cvp.types import override
from cvp.variables import VERBOSE_LEVEL_1 as VL1
from cvp.widgets.window import Window

OVERLAY_WINDOW_FLAGS: Final[int] = (
    imgui.WINDOW_NO_DECORATION
    | imgui.WINDOW_ALWAYS_AUTO_RESIZE
    | imgui.WINDOW_NO_SAVED_SETTINGS
    | imgui.WINDOW_NO_NAV
    | imgui.WINDOW_NO_MOVE
)


class OverlayWindow(Window[OverlaySection]):
    def __init__(self, context: Context):
        super().__init__(
            context=context,
            section=context.config.overlay,
            title="Overlay",
            closable=False,
            flags=OVERLAY_WINDOW_FLAGS,
        )
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

    def get_framerate_color(self, framerate: float) -> Sequence[float]:
        if framerate >= self.section.fps_warning_threshold:
            return self.section.normal_color
        elif framerate >= self.section.fps_error_threshold:
            return self.section.warning_color
        else:
            return self.section.error_color

    @override
    def begin(self) -> Tuple[bool, bool]:
        pos_x, pos_y = self.window_position
        pivot_x, pivot_y = self.window_pivot
        imgui.set_next_window_position(pos_x, pos_y, imgui.ALWAYS, pivot_x, pivot_y)
        imgui.set_next_window_bg_alpha(self.section.alpha)
        return super().begin()

    @override
    def on_process(self) -> None:
        io = imgui.get_io()
        framerate_color = self.get_framerate_color(io.framerate)
        imgui.text_colored(f"FPS: {floor(io.framerate)}", *framerate_color)

        if self.context.debug and self.context.verbose >= VL1:
            imgui.text(f"Vertices: {io.metrics_render_vertices}")
            imgui.text(f"Indices: {io.metrics_render_indices}")
            imgui.text(f"Visible Windows: {io.metrics_render_windows}")

        imgui.separator()

        usage = self._usage.update_interval()
        imgui.text(f"CPU: {usage.cpu:3.1f}%")
        imgui.text(f"VMEM: {usage.vmem:3.1f}%")

        imgui.separator()
        mouse_pos = imgui.get_mouse_pos()
        imgui.text(f"Mouse: {floor(mouse_pos.x)}, {floor(mouse_pos.y)}")

        if begin_popup_context_window().opened:
            try:
                self.on_popup_context_window()
            finally:
                end_popup_context_window()

    def on_popup_context_window(self) -> None:
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
