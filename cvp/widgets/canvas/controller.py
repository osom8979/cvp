# -*- coding: utf-8 -*-

from math import fmod
from typing import Final, Optional

import imgui

from cvp.flow.datas import Canvas as CanvasProps
from cvp.imgui.drag_float2 import drag_float2
from cvp.imgui.draw_list import create_empty_draw_list, get_window_draw_list
from cvp.imgui.input_float2 import input_float2
from cvp.imgui.push_style_var import style_disable_input
from cvp.imgui.slider_float import slider_float
from cvp.types.shapes import ROI, Point

_BUTTON_LEFT_FLAG: Final[int] = imgui.BUTTON_MOUSE_BUTTON_LEFT
_BUTTON_MIDDLE_FLAG: Final[int] = imgui.BUTTON_MOUSE_BUTTON_MIDDLE
_BUTTON_RIGHT_FLAG: Final[int] = imgui.BUTTON_MOUSE_BUTTON_RIGHT

ALL_BUTTON_FLAGS: Final[int] = (
    _BUTTON_LEFT_FLAG | _BUTTON_MIDDLE_FLAG | _BUTTON_RIGHT_FLAG
)

BUTTON_LEFT: Final[int] = imgui.MOUSE_BUTTON_LEFT
BUTTON_MIDDLE: Final[int] = imgui.MOUSE_BUTTON_MIDDLE
BUTTON_RIGHT: Final[int] = imgui.MOUSE_BUTTON_RIGHT


class CanvasController:
    def __init__(self, canvas_props: Optional[CanvasProps] = None):
        self.canvas_props = canvas_props if canvas_props else CanvasProps()

        self.draw_list = create_empty_draw_list()
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
        self.control_button_flags = ALL_BUTTON_FLAGS
        self.control_lock_threshold = -1.0

        self.left_clicked = False
        self.middle_clicked = False
        self.right_clicked = False

        self.left_dragging = False
        self.middle_dragging = False
        self.right_dragging = False

        self.ctrl_down = False
        self.alt_down = False
        self.shift_down = False
        self.super_down = False

        self.hovering = False
        self.activated = False

    @property
    def canvas_roi(self):
        return (
            self.canvas_pos[0],
            self.canvas_pos[1],
            self.canvas_pos[0] + self.canvas_size[0],
            self.canvas_pos[1] + self.canvas_size[1],
        )

    @property
    def pan_x(self) -> float:
        return self.canvas_props.pan_x

    @pan_x.setter
    def pan_x(self, value: float) -> None:
        self.canvas_props.pan_x = value

    @property
    def pan_y(self) -> float:
        return self.canvas_props.pan_y

    @pan_y.setter
    def pan_y(self, value: float) -> None:
        self.canvas_props.pan_y = value

    @property
    def zoom(self) -> float:
        return self.canvas_props.zoom

    @zoom.setter
    def zoom(self, value: float) -> None:
        self.canvas_props.zoom = value

    @property
    def alpha(self) -> float:
        return self.canvas_props.alpha

    @alpha.setter
    def alpha(self, value: float) -> None:
        self.canvas_props.alpha = value

    def reset(self):
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.zoom = 1.0
        self.alpha = 1.0

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

    def slider_alpha(self, dryrun=False):
        result = slider_float(
            self.alpha_label,
            self.alpha,
            self.alpha_min,
            self.alpha_max,
            self.alpha_fmt,
        )
        if not dryrun and result:
            self.alpha = result.value
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

    def render_controllers(self, dryrun=False) -> None:
        self.drag_pan(dryrun=dryrun)
        self.slider_zoom(dryrun=dryrun)
        self.slider_alpha(dryrun=dryrun)
        with style_disable_input():
            self.input_local_pos()
            self.input_canvas_pos()

    def point_in_canvas_rect(self, point: Point) -> bool:
        cx, cy = self.canvas_pos
        cw, ch = self.canvas_size
        return cx <= point[0] <= cx + cw and cy <= point[1] <= cy + ch

    def canvas_to_screen_coords(self, canvas_point: Point) -> Point:
        cx, cy = self.canvas_pos
        x = cx + (canvas_point[0] + self.pan_x) * self.zoom
        y = cy + (canvas_point[1] + self.pan_y) * self.zoom
        return x, y

    def local_origin_to_screen_coords(self) -> Point:
        return self.canvas_to_screen_coords((0.0, 0.0))

    def mouse_to_screen_coords(self) -> Point:
        return self.canvas_to_screen_coords(self.mouse_pos)

    def canvas_to_screen_roi(self, canvas_roi: ROI) -> ROI:
        canvas_p1 = canvas_roi[0], canvas_roi[1]
        canvas_p2 = canvas_roi[2], canvas_roi[3]
        p1 = self.canvas_to_screen_coords(canvas_p1)
        p2 = self.canvas_to_screen_coords(canvas_p2)
        return p1[0], p1[1], p2[0], p2[1]

    def screen_to_canvas_coords(self, screen_point: Point) -> Point:
        cx, cy = self.canvas_pos
        x = (screen_point[0] - cx) / self.zoom - self.pan_x
        y = (screen_point[1] - cy) / self.zoom - self.pan_y
        return x, y

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

    def vertical_grid_lines(self, step: float):
        cx, cy = self.canvas_pos
        cw, ch = self.canvas_size

        if step <= 0:
            raise ValueError("The 'step' value must be greater than 0")
        if self.zoom <= 0:
            raise ValueError("The 'zoom' value must be greater than 0")

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

    def horizontal_grid_lines(self, step: float):
        cx, cy = self.canvas_pos
        cw, ch = self.canvas_size

        if step <= 0:
            raise ValueError("The 'step' value must be greater than 0")
        if self.zoom <= 0:
            raise ValueError("The 'zoom' value must be greater than 0")

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
        imgui.invisible_button("##ControlButton", cw, ch, self.control_button_flags)

        self.left_clicked = imgui.is_mouse_clicked(BUTTON_LEFT)
        self.middle_clicked = imgui.is_mouse_clicked(BUTTON_MIDDLE)
        self.right_clicked = imgui.is_mouse_clicked(BUTTON_RIGHT)

        self.left_dragging = self.is_mouse_dragging(BUTTON_LEFT)
        self.middle_dragging = self.is_mouse_dragging(BUTTON_MIDDLE)
        self.right_dragging = self.is_mouse_dragging(BUTTON_RIGHT)

        self.ctrl_down = io.key_ctrl
        self.alt_down = io.key_alt
        self.shift_down = io.key_shift
        self.super_down = io.key_super

        self.hovering = imgui.is_item_hovered()
        self.activated = imgui.is_item_active()

        if self.activated and self.middle_dragging:
            self.pan_x += io.mouse_delta.x / self.zoom
            self.pan_y += io.mouse_delta.y / self.zoom
        elif self.activated and self.alt_down and self.left_dragging:
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
