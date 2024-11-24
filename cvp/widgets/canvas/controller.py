# -*- coding: utf-8 -*-

from math import fmod
from typing import Final, Optional, Tuple

import imgui

from cvp.flow.datas import Canvas as CanvasProps
from cvp.imgui.drag_float2 import drag_float2
from cvp.imgui.input_float2 import input_float2
from cvp.imgui.push_style_var import style_disable_input
from cvp.imgui.slider_float import slider_float
from cvp.types.shapes import ROI, Point

BUTTON_LEFT: Final[int] = imgui.BUTTON_MOUSE_BUTTON_LEFT
BUTTON_MIDDLE: Final[int] = imgui.BUTTON_MOUSE_BUTTON_MIDDLE
BUTTON_RIGHT: Final[int] = imgui.BUTTON_MOUSE_BUTTON_RIGHT


class CanvasController:
    def __init__(self, canvas_props: Optional[CanvasProps] = None):
        self.canvas_props = canvas_props if canvas_props else CanvasProps()

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
        self.control_button_flags = BUTTON_LEFT | BUTTON_MIDDLE | BUTTON_RIGHT
        self.control_button = imgui.MOUSE_BUTTON_LEFT
        self.control_threshold = -1.0

        self.hovering = False
        self.activated = False
        self.dragging = False

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

    def canvas_to_screen_coords(
        self,
        canvas_point: Point,
        cursor_screen_pos: Optional[Point] = None,
    ) -> Point:
        if cursor_screen_pos is None:
            cursor_screen_pos = imgui.get_cursor_screen_pos()
        assert cursor_screen_pos is not None
        cx, cy = cursor_screen_pos
        assert isinstance(cx, float)
        assert isinstance(cy, float)
        x = cx + (canvas_point[0] + self.pan_x) * self.zoom
        y = cy + (canvas_point[1] + self.pan_y) * self.zoom
        return x, y

    def local_origin_to_screen_coords(
        self,
        cursor_screen_pos: Optional[Point] = None,
    ) -> Point:
        return self.canvas_to_screen_coords((0.0, 0.0), cursor_screen_pos)

    def canvas_to_screen_roi(
        self,
        canvas_roi: ROI,
        cursor_screen_pos: Optional[Point] = None,
    ) -> ROI:
        if cursor_screen_pos is None:
            cursor_screen_pos = imgui.get_cursor_screen_pos()
        assert cursor_screen_pos is not None
        canvas_p1 = canvas_roi[0], canvas_roi[1]
        canvas_p2 = canvas_roi[2], canvas_roi[3]
        p1 = self.canvas_to_screen_coords(canvas_p1, cursor_screen_pos)
        p2 = self.canvas_to_screen_coords(canvas_p2, cursor_screen_pos)
        return p1[0], p1[1], p2[0], p2[1]

    def screen_to_canvas_coords(
        self,
        screen_point: Point,
        cursor_screen_pos: Optional[Point] = None,
    ) -> Point:
        if cursor_screen_pos is None:
            cursor_screen_pos = imgui.get_cursor_screen_pos()
        assert cursor_screen_pos is not None
        cx, cy = cursor_screen_pos
        assert isinstance(cx, float)
        assert isinstance(cy, float)
        x = (screen_point[0] - cx) / self.zoom - self.pan_x
        y = (screen_point[1] - cy) / self.zoom - self.pan_y
        return x, y

    @property
    def lock_threshold_for_pan(self) -> float:
        """
        Pan (we use a zero mouse threshold when there's no context menu)
        You may decide to make that threshold dynamic based on whether
        the mouse is hovering something etc.
        """
        return self.control_threshold if self.has_context_menu else 0.0

    def is_dragging_for_pan(self) -> bool:
        return imgui.is_mouse_dragging(self.control_button, self.lock_threshold_for_pan)

    def do_control(
        self,
        cursor_screen_pos: Optional[Tuple[float, float]] = None,
        content_region_available: Optional[Tuple[float, float]] = None,
    ) -> None:
        if cursor_screen_pos is None:
            cursor_screen_pos = imgui.get_cursor_screen_pos()
        if content_region_available is None:
            content_region_available = imgui.get_content_region_available()

        assert cursor_screen_pos is not None
        assert content_region_available is not None
        cx, cy = cursor_screen_pos
        cw, ch = content_region_available

        assert isinstance(cx, float)
        assert isinstance(cy, float)
        assert isinstance(cw, float)
        assert isinstance(ch, float)

        # Using `imgui.invisible_button()` as a convenience
        # 1) it will advance the layout cursor and
        # 2) allows us to use `is_item_hovered()`/`is_item_active()`
        imgui.invisible_button("##ControlButton", cw, ch, self.control_button_flags)

        self.hovering = imgui.is_item_hovered()
        self.activated = imgui.is_item_active()
        self.dragging = self.is_dragging_for_pan()

        io = imgui.get_io()
        if self.activated:
            if self.dragging:
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

            canvas_pos = self.screen_to_canvas_coords((mx, my), cursor_screen_pos)
            self.canvas_pos_x = canvas_pos[0]
            self.canvas_pos_y = canvas_pos[1]

    def vertical_grid_lines(
        self,
        step: float,
        cursor_screen_pos: Optional[Tuple[float, float]] = None,
        content_region_available: Optional[Tuple[float, float]] = None,
    ):
        if cursor_screen_pos is None:
            cursor_screen_pos = imgui.get_cursor_screen_pos()
        if content_region_available is None:
            content_region_available = imgui.get_content_region_available()

        assert cursor_screen_pos is not None
        assert content_region_available is not None
        cx, cy = cursor_screen_pos
        cw, ch = content_region_available

        assert isinstance(cx, float)
        assert isinstance(cy, float)
        assert isinstance(cw, float)
        assert isinstance(ch, float)

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

    def horizontal_grid_lines(
        self,
        step: float,
        cursor_screen_pos: Optional[Tuple[float, float]] = None,
        content_region_available: Optional[Tuple[float, float]] = None,
    ):
        if cursor_screen_pos is None:
            cursor_screen_pos = imgui.get_cursor_screen_pos()
        if content_region_available is None:
            content_region_available = imgui.get_content_region_available()

        assert cursor_screen_pos is not None
        assert content_region_available is not None
        cx, cy = cursor_screen_pos
        cw, ch = content_region_available

        assert isinstance(cx, float)
        assert isinstance(cy, float)
        assert isinstance(cw, float)
        assert isinstance(ch, float)

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
