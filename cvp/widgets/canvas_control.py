# -*- coding: utf-8 -*-

from math import fmod
from typing import Final, Optional, Tuple

import imgui

from cvp.gui import drag_float2, slider_float
from cvp.types import override
from cvp.widgets.widget import WidgetInterface

BUTTON_LEFT: Final[int] = imgui.BUTTON_MOUSE_BUTTON_LEFT
BUTTON_MIDDLE: Final[int] = imgui.BUTTON_MOUSE_BUTTON_MIDDLE
BUTTON_RIGHT: Final[int] = imgui.BUTTON_MOUSE_BUTTON_RIGHT


class CanvasControl(WidgetInterface):
    def __init__(self):
        self.pan_label = "Pan"
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.pan_speed = 0.1
        self.pan_min = 0.0
        self.pan_max = 0.0
        self.pan_fmt = "%.1f"
        self.pan_flags = 0

        self.zoom_label = "Zoom"
        self.zoom = 1.0
        self.zoom_step = 0.02
        self.zoom_min = 0.01
        self.zoom_max = 10.0
        self.zoom_fmt = "%.2f"
        self.zoom_flags = 0

        self.alpha_label = "Alpha"
        self.alpha = 1.0
        self.alpha_min = 0.0
        self.alpha_max = 1.0
        self.alpha_fmt = "%.3f"

        self.button_flags = BUTTON_LEFT | BUTTON_MIDDLE | BUTTON_RIGHT

    def reset(self):
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.zoom = 1.0
        self.alpha = 1.0

    def drag_pan(self):
        return drag_float2(
            self.pan_label,
            self.pan_x,
            self.pan_y,
            self.pan_speed,
            self.pan_min,
            self.pan_max,
            self.pan_fmt,
            self.pan_flags,
        )

    def slider_zoom(self):
        return slider_float(
            self.zoom_label,
            self.zoom,
            self.zoom_min,
            self.zoom_max,
            self.zoom_fmt,
            self.zoom_flags,
        )

    def slider_alpha(self):
        return slider_float(
            self.alpha_label,
            self.alpha,
            self.alpha_min,
            self.alpha_max,
            self.alpha_fmt,
        )

    @override
    def on_process(self) -> None:
        if pan := self.drag_pan():
            self.pan_x = pan.value0
            self.pan_y = pan.value1

        if zoom := self.slider_zoom():
            self.zoom = zoom.value

        if alpha := self.slider_alpha():
            self.alpha = alpha.value

    def do_control(
        self,
        canvas_size: Optional[Tuple[float, float]] = None,
        pan_button=imgui.MOUSE_BUTTON_MIDDLE,
        has_context_menu=False,
    ) -> None:
        cw, ch = canvas_size if canvas_size else imgui.get_content_region_available()

        # Using `imgui.invisible_button()` as a convenience
        # 1) it will advance the layout cursor and
        # 2) allows us to use `is_item_hovered()`/`is_item_active()`
        imgui.invisible_button("## CanvasButton", cw, ch, self.button_flags)

        is_hovered = imgui.is_item_hovered()
        is_active = imgui.is_item_active()

        io = imgui.get_io()
        if is_active:
            # Pan (we use a zero mouse threshold when there's no context menu)
            # You may decide to make that threshold dynamic based on whether
            # the mouse is hovering something etc.
            lock_threshold_for_pan = -1.0 if has_context_menu else 0.0
            is_dragging = imgui.is_mouse_dragging(pan_button, lock_threshold_for_pan)
            if is_dragging:
                self.pan_x += io.mouse_delta.x / self.zoom
                self.pan_y += io.mouse_delta.y / self.zoom

        if is_hovered and io.mouse_wheel != 0:
            if io.mouse_wheel > 0:
                self.zoom += self.zoom_step
            elif io.mouse_wheel < 0:
                self.zoom -= self.zoom_step

        if self.zoom > self.zoom_max:
            self.zoom = self.zoom_max
        elif self.zoom < self.zoom_min:
            self.zoom = self.zoom_min

    def vertical_lines(
        self,
        step: float,
        canvas_pos: Optional[Tuple[float, float]] = None,
        canvas_size: Optional[Tuple[float, float]] = None,
    ):
        cx, cy = canvas_pos if canvas_pos else imgui.get_cursor_screen_pos()
        cw, ch = canvas_size if canvas_size else imgui.get_content_region_available()
        assert isinstance(cx, float)
        assert isinstance(cy, float)
        assert isinstance(cw, float)
        assert isinstance(ch, float)

        result = list()
        x = fmod(self.pan_x * self.zoom, step * self.zoom)
        while x < cw:
            x1 = cx + x
            y1 = cy
            x2 = cx + x
            y2 = cy + ch
            result.append((x1, y1, x2, y2))
            x += step * self.zoom
        return result

    def horizontal_lines(
        self,
        step: float,
        canvas_pos: Optional[Tuple[float, float]] = None,
        canvas_size: Optional[Tuple[float, float]] = None,
    ):
        cx, cy = canvas_pos if canvas_pos else imgui.get_cursor_screen_pos()
        cw, ch = canvas_size if canvas_size else imgui.get_content_region_available()
        assert isinstance(cx, float)
        assert isinstance(cy, float)
        assert isinstance(cw, float)
        assert isinstance(ch, float)

        result = list()
        y = fmod(self.pan_y * self.zoom, step * self.zoom)
        while y < ch:
            x1 = cx
            y1 = cy + y
            x2 = cx + cw
            y2 = cy + y
            result.append((x1, y1, x2, y2))
            y += step * self.zoom
        return result

    def calc_coord(
        self,
        point: Tuple[float, float],
        canvas_pos: Optional[Tuple[float, float]] = None,
    ):
        cx, cy = canvas_pos if canvas_pos else imgui.get_cursor_screen_pos()
        assert isinstance(cx, float)
        assert isinstance(cy, float)
        x = cx + (point[0] + self.pan_x) * self.zoom
        y = cy + (point[1] + self.pan_y) * self.zoom
        return x, y

    def calc_roi(
        self,
        roi: Tuple[float, float, float, float],
        canvas_pos: Optional[Tuple[float, float]] = None,
    ):
        p1 = self.calc_coord((roi[0], roi[1]), canvas_pos)
        p2 = self.calc_coord((roi[2], roi[3]), canvas_pos)
        return p1, p2
