# -*- coding: utf-8 -*-

from math import fmod
from typing import Final, Tuple

import imgui

from cvp.imgui.drag_float2 import drag_float2
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.draw_list.types import DrawList
from cvp.imgui.input_float2 import input_float2
from cvp.imgui.push_style_var import style_disable_input
from cvp.imgui.slider_float import slider_float
from cvp.types.shapes import ROI, Point
from cvp.widgets.canvas.controller.result import ControllerResult

LBUTTON_FLAG: Final[int] = imgui.BUTTON_MOUSE_BUTTON_LEFT
MBUTTON_FLAG: Final[int] = imgui.BUTTON_MOUSE_BUTTON_MIDDLE
RBUTTON_FLAG: Final[int] = imgui.BUTTON_MOUSE_BUTTON_RIGHT
ALL_BUTTON_FLAGS: Final[int] = LBUTTON_FLAG | MBUTTON_FLAG | RBUTTON_FLAG

BUTTON_LEFT: Final[int] = imgui.MOUSE_BUTTON_LEFT
BUTTON_MIDDLE: Final[int] = imgui.MOUSE_BUTTON_MIDDLE
BUTTON_RIGHT: Final[int] = imgui.MOUSE_BUTTON_RIGHT


class CanvasController:
    def __init__(self):
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.zoom = 1.0

        self.draw_list = DrawList()
        self.mouse_pos = 0.0, 0.0
        self.canvas_pos = 0.0, 0.0
        self.canvas_size = 0.0, 0.0

        self.pan_label = "Pan"
        self.pan_speed = 0.1
        self.pan_min = 0.0
        self.pan_max = 0.0
        self.pan_fmt = "%.1f"
        self.pan_flags = 0

        self.zoom_label = "Zoom"
        self.zoom_step = 0.02
        self.zoom_min = 0.01
        self.zoom_max = 10.0
        self.zoom_fmt = "%.2f"
        self.zoom_flags = 0

        self.alpha_label = "Alpha"
        self.alpha_min = 0.0
        self.alpha_max = 1.0
        self.alpha_fmt = "%.3f"

        self.local_pos_label = "Local"
        self.local_pos_x = 0.0
        self.local_pos_y = 0.0
        self.local_pos_fmt = "%.3f"
        self.local_pos_flags = imgui.INPUT_TEXT_READ_ONLY

        self.canvas_pos_label = "Canvas"
        self.canvas_pos_x = 0.0
        self.canvas_pos_y = 0.0
        self.canvas_pos_fmt = "%.3f"
        self.canvas_pos_flags = imgui.INPUT_TEXT_READ_ONLY

        self.has_context_menu = False
        self.control_identifier = "ControlInvisibleButton"
        self.control_flags = ALL_BUTTON_FLAGS
        self.control_lock_threshold = -1.0

        self.left_clicked = False
        self.middle_clicked = False
        self.right_clicked = False

        self.prev_left_dragging = False
        self.prev_middle_dragging = False
        self.prev_right_dragging = False

        self.left_dragging = False
        self.middle_dragging = False
        self.right_dragging = False

        self.left_down = False
        self.middle_down = False
        self.right_down = False

        self.left_up = False
        self.middle_up = False
        self.right_up = False

        self.ctrl_down = False
        self.alt_down = False
        self.shift_down = False

        self.hovering = False
        self.deactivated = False
        self.activating = False

    @property
    def is_pan_mode(self) -> bool:
        # Pressing the ALT button switches to 'Canvas Pan Mode'
        return self.alt_down

    @property
    def frame_padding(self) -> Tuple[int, int]:
        return imgui.get_style().frame_padding

    @property
    def window_padding(self) -> Tuple[int, int]:
        return imgui.get_style().window_padding

    @property
    def item_spacing(self) -> Tuple[int, int]:
        return imgui.get_style().item_spacing

    @property
    def item_inner_spacing(self) -> Tuple[int, int]:
        return imgui.get_style().item_inner_spacing

    @property
    def mx(self):
        return self.mouse_pos[0]

    @property
    def my(self):
        return self.mouse_pos[1]

    @property
    def cx(self):
        return self.canvas_pos[0]

    @property
    def cy(self):
        return self.canvas_pos[1]

    @property
    def cw(self):
        return self.canvas_size[0]

    @property
    def ch(self):
        return self.canvas_size[1]

    @property
    def p1(self):
        return self.cx, self.cy

    @property
    def p2(self):
        return self.cx + self.cw, self.cy + self.ch

    @property
    def canvas_roi(self):
        return self.cx, self.cy, self.cx + self.cw, self.cy + self.ch

    @property
    def pan(self) -> Point:
        return self.pan_x, self.pan_y

    @pan.setter
    def pan(self, value: Point) -> None:
        self.pan_x = value[0]
        self.pan_y = value[1]

    def as_unformatted_text(self):
        return (
            f"Pen: {self.pan_x:.02f}, {self.pan_y:.02f}\n"
            f"Zoom: {self.zoom:.02f}\n"
            f"Mouse pos: {self.mx:.02f}, {self.my:.02f}\n"
            f"Canvas pos: {self.cx:.02f}, {self.cy:.02f}\n"
            f"Canvas size: {self.cw:.02f}, {self.ch:.02f}\n"
            f"Left clicked: {self.left_clicked}\n"
            f"Middle clicked: {self.middle_clicked}\n"
            f"Right clicked: {self.right_clicked}\n"
            f"Left dragging: {self.left_dragging}\n"
            f"Middle dragging: {self.middle_dragging}\n"
            f"Right dragging: {self.right_dragging}\n"
            f"Left down: {self.left_down}\n"
            f"Middle down: {self.middle_down}\n"
            f"Right down: {self.right_down}\n"
            f"Left up: {self.left_up}\n"
            f"Middle up: {self.middle_up}\n"
            f"Right up: {self.right_up}\n"
            f"Ctrl down: {self.ctrl_down}\n"
            f"Alt down: {self.alt_down}\n"
            f"Shift down: {self.shift_down}\n"
            f"Hovering: {self.hovering}\n"
            f"Activated: {self.activating}\n"
            f"Deactivated: {self.deactivated}\n"
        )

    def reset(self):
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.zoom = 1.0

    def drag_pan(self, dryrun=False):
        result = drag_float2(
            self.pan_label,
            self.pan_x,
            self.pan_y,
            self.pan_speed,
            self.pan_min,
            self.pan_max,
            self.pan_fmt,
            self.pan_flags,
        )
        if not dryrun and result:
            self.pan_x = result.value0
            self.pan_y = result.value1
        return result

    def slider_zoom(self, dryrun=False):
        result = slider_float(
            self.zoom_label,
            self.zoom,
            self.zoom_min,
            self.zoom_max,
            self.zoom_fmt,
            self.zoom_flags,
        )
        if not dryrun and result:
            self.zoom = result.value
        return result

    def input_local_pos(self):
        return input_float2(
            self.local_pos_label,
            self.local_pos_x,
            self.local_pos_y,
            self.local_pos_fmt,
            self.local_pos_flags,
        )

    def input_canvas_pos(self):
        return input_float2(
            self.canvas_pos_label,
            self.canvas_pos_x,
            self.canvas_pos_y,
            self.canvas_pos_fmt,
            self.canvas_pos_flags,
        )

    def tree_debugging(self) -> None:
        if imgui.tree_node("Debugging"):
            try:
                message = self.as_unformatted_text()
                imgui.text_unformatted(message.strip())
            finally:
                imgui.tree_pop()

    def render_controllers(self, dryrun=False, debugging=False) -> ControllerResult:
        pan_result = self.drag_pan(dryrun=dryrun)
        zoom_result = self.slider_zoom(dryrun=dryrun)

        with style_disable_input():
            self.input_local_pos()
            self.input_canvas_pos()

        if debugging:
            self.tree_debugging()

        changed = pan_result.clicked and zoom_result.changed
        return ControllerResult(changed, self.pan_x, self.pan_y, self.zoom)

    def point_in_canvas_rect(self, point: Point) -> bool:
        x, y = point
        cx, cy = self.canvas_pos
        cw, ch = self.canvas_size
        return cx <= x <= cx + cw and cy <= y <= cy + ch

    def canvas_to_screen_coords(self, point: Point) -> Point:
        x = self.cx + (point[0] + self.pan_x) * self.zoom
        y = self.cy + (point[1] + self.pan_y) * self.zoom
        return x, y

    def local_origin_to_screen_coords(self) -> Point:
        return self.canvas_to_screen_coords((0.0, 0.0))

    def mouse_to_screen_coords(self) -> Point:
        return self.canvas_to_screen_coords(self.mouse_pos)

    def canvas_to_screen_roi(self, roi: ROI) -> ROI:
        p1 = self.canvas_to_screen_coords((roi[0], roi[1]))
        p2 = self.canvas_to_screen_coords((roi[2], roi[3]))
        return p1[0], p1[1], p2[0], p2[1]

    def screen_to_canvas_coords(self, point: Point) -> Point:
        x = (point[0] - self.cx) / self.zoom - self.pan_x
        y = (point[1] - self.cy) / self.zoom - self.pan_y
        return x, y

    def mouse_to_canvas_coords(self) -> Point:
        return self.screen_to_canvas_coords(self.mouse_pos)

    @property
    def lock_threshold(self) -> float:
        """
        Pan (we use a zero mouse threshold when there's no context menu)
        You may decide to make that threshold dynamic based on whether
        the mouse is hovering something etc.
        """
        return self.control_lock_threshold if self.has_context_menu else -1.0

    def is_mouse_dragging(self, button: int) -> bool:
        return imgui.is_mouse_dragging(button, self.lock_threshold)

    def is_mouse_button_left_dragging(self) -> bool:
        return self.is_mouse_dragging(BUTTON_LEFT)

    def is_mouse_button_middle_dragging(self) -> bool:
        return self.is_mouse_dragging(BUTTON_MIDDLE)

    def is_mouse_button_right_dragging(self) -> bool:
        return self.is_mouse_dragging(BUTTON_RIGHT)

    def vertical_grid_lines(self, step: float):
        if step <= 0:
            raise ValueError("The 'step' value must be greater than 0")
        if self.zoom <= 0:
            raise ValueError("The 'zoom' value must be greater than 0")

        result = list()
        x = fmod(self.pan_x * self.zoom, step * self.zoom)
        while x < self.cw:
            x1 = self.cx + x
            y1 = self.cy
            x2 = self.cx + x
            y2 = self.cy + self.ch
            result.append((x1, y1, x2, y2))
            x += step * self.zoom
        return result

    def horizontal_grid_lines(self, step: float):
        if step <= 0:
            raise ValueError("The 'step' value must be greater than 0")
        if self.zoom <= 0:
            raise ValueError("The 'zoom' value must be greater than 0")

        result = list()
        y = fmod(self.pan_y * self.zoom, step * self.zoom)
        while y < self.ch:
            x1 = self.cx
            y1 = self.cy + y
            x2 = self.cx + self.cw
            y2 = self.cy + y
            result.append((x1, y1, x2, y2))
            y += step * self.zoom
        return result

    def control(self) -> None:
        mx, my = imgui.get_mouse_pos()
        cx, cy = imgui.get_cursor_screen_pos()
        cw, ch = imgui.get_content_region_available()
        assert isinstance(mx, float)
        assert isinstance(my, float)
        assert isinstance(cx, float)
        assert isinstance(cy, float)
        assert isinstance(cw, float)
        assert isinstance(ch, float)
        self.draw_list = get_window_draw_list()
        self.mouse_pos = mx, my
        self.canvas_pos = cx, cy
        self.canvas_size = cw, ch

        cx, cy = self.canvas_pos
        cw, ch = self.canvas_size
        io = imgui.get_io()

        # Using `imgui.invisible_button()` as a convenience
        # 1) it will advance the layout cursor and
        # 2) allows us to use `is_item_hovered()`/`is_item_active()`
        imgui.invisible_button(self.control_identifier, cw, ch, self.control_flags)

        self.left_clicked = imgui.is_mouse_clicked(BUTTON_LEFT)
        self.middle_clicked = imgui.is_mouse_clicked(BUTTON_MIDDLE)
        self.right_clicked = imgui.is_mouse_clicked(BUTTON_RIGHT)

        _left_dragging = self.is_mouse_dragging(BUTTON_LEFT)
        _middle_dragging = self.is_mouse_dragging(BUTTON_MIDDLE)
        _right_dragging = self.is_mouse_dragging(BUTTON_RIGHT)
        self.prev_left_dragging = self.left_dragging
        self.prev_middle_dragging = self.middle_dragging
        self.prev_right_dragging = self.right_dragging
        self.left_dragging = _left_dragging
        self.middle_dragging = _middle_dragging
        self.right_dragging = _right_dragging

        _left_down = bool(io.mouse_down[imgui.MOUSE_BUTTON_LEFT])
        _middle_down = bool(io.mouse_down[imgui.MOUSE_BUTTON_MIDDLE])
        _right_down = bool(io.mouse_down[imgui.MOUSE_BUTTON_RIGHT])
        self.left_up = self.left_down and not _left_down
        self.middle_up = self.middle_down and not _middle_down
        self.right_up = self.right_down and not _right_down
        self.left_down = _left_down
        self.middle_down = _middle_down
        self.right_down = _right_down

        self.ctrl_down = io.key_ctrl
        self.alt_down = io.key_alt
        self.shift_down = io.key_shift

        self.hovering = imgui.is_item_hovered()
        _activated = imgui.is_item_active()
        self.deactivated = self.activating and not _activated
        self.activating = _activated

        if self.activating:
            if self.middle_dragging:
                self.pan_x += io.mouse_delta.x / self.zoom
                self.pan_y += io.mouse_delta.y / self.zoom
            elif self.alt_down and self.left_dragging:
                self.pan_x += io.mouse_delta.x / self.zoom
                self.pan_y += io.mouse_delta.y / self.zoom

        if self.hovering and io.mouse_wheel != 0:
            if io.mouse_wheel > 0:
                self.zoom += self.zoom_step
            elif io.mouse_wheel < 0:
                self.zoom -= self.zoom_step

        if self.zoom > self.zoom_max:
            self.zoom = self.zoom_max
        elif self.zoom < self.zoom_min:
            self.zoom = self.zoom_min

        if self.hovering:
            mx, my = imgui.get_mouse_pos()
            assert isinstance(mx, float)
            assert isinstance(my, float)
            self.local_pos_x = mx - cx
            self.local_pos_y = my - cy

            canvas_pos = self.screen_to_canvas_coords((mx, my))
            self.canvas_pos_x = canvas_pos[0]
            self.canvas_pos_y = canvas_pos[1]
