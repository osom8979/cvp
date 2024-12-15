# -*- coding: utf-8 -*-

from math import fmod
from typing import Tuple, Union

import imgui

from cvp.imgui.drag_float2 import drag_float2
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.draw_list.types import DrawList
from cvp.imgui.flags.button import ALL_BUTTON_FLAGS
from cvp.imgui.flags.mouse import MouseButton
from cvp.imgui.input_float2 import input_float2
from cvp.imgui.push_style_var import style_disable_input
from cvp.imgui.slider_float import slider_float
from cvp.patterns.state_watcher import StateWatcher
from cvp.types.shapes import ROI, Point
from cvp.widgets.canvas.controller.result import ControllerResult


class CanvasController:
    def __init__(self):
        self._pan_x = StateWatcher(0.0, 0.0)
        self._pan_y = StateWatcher(0.0, 0.0)
        self._zoom = StateWatcher(1.0, 1.0)

        self._draw_list = DrawList()
        self._mouse_pos = 0.0, 0.0
        self._canvas_pos = 0.0, 0.0
        self._canvas_size = 0.0, 0.0

        self._pan_label = "Pan"
        self._pan_speed = 0.1
        self._pan_min = 0.0
        self._pan_max = 0.0
        self._pan_fmt = "%.1f"
        self._pan_flags = 0

        self._zoom_label = "Zoom"
        self._zoom_step = 0.02
        self._zoom_min = 0.01
        self._zoom_max = 10.0
        self._zoom_fmt = "%.2f"
        self._zoom_flags = 0

        self._local_pos_label = "Local"
        self._local_pos_x = 0.0
        self._local_pos_y = 0.0
        self._local_pos_fmt = "%.3f"
        self._local_pos_flags = imgui.INPUT_TEXT_READ_ONLY

        self._canvas_pos_label = "Canvas"
        self._canvas_pos_x = 0.0
        self._canvas_pos_y = 0.0
        self._canvas_pos_fmt = "%.3f"
        self._canvas_pos_flags = imgui.INPUT_TEXT_READ_ONLY

        self._has_context_menu = False
        self._control_identifier = type(self).__name__
        self._control_flags = int(ALL_BUTTON_FLAGS)
        self._lock_threshold = -1.0

        self._activating = StateWatcher(False, False)
        self._hovering = StateWatcher(False, False)

        self._left_dragging = StateWatcher(False, False)
        self._middle_dragging = StateWatcher(False, False)
        self._right_dragging = StateWatcher(False, False)

        self._left_down = StateWatcher(False, False)
        self._middle_down = StateWatcher(False, False)
        self._right_down = StateWatcher(False, False)

        self._shift_down = StateWatcher(False, False)
        self._ctrl_down = StateWatcher(False, False)
        self._alt_down = StateWatcher(False, False)

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
        return self._mouse_pos[0]

    @property
    def my(self):
        return self._mouse_pos[1]

    @property
    def cx(self):
        return self._canvas_pos[0]

    @property
    def cy(self):
        return self._canvas_pos[1]

    @property
    def cw(self):
        return self._canvas_size[0]

    @property
    def ch(self):
        return self._canvas_size[1]

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
    def pan_x(self):
        return self._pan_x.value

    @pan_x.setter
    def pan_x(self, value: float) -> None:
        self._pan_x.value = value

    @property
    def pan_y(self):
        return self._pan_y.value

    @pan_y.setter
    def pan_y(self, value: float) -> None:
        self._pan_y.value = value

    @property
    def zoom(self):
        return self._zoom.value

    @zoom.setter
    def zoom(self, value: float) -> None:
        self._zoom.value = value

    @property
    def pan(self) -> Point:
        return self._pan_x.value, self._pan_y.value

    @pan.setter
    def pan(self, value: Point) -> None:
        self._pan_x.value = value[0]
        self._pan_y.value = value[1]

    @property
    def activating(self):
        return self._activating.value

    @property
    def hovering(self):
        return self._hovering.value

    @property
    def left_dragging(self):
        return self._left_dragging.value

    @property
    def middle_dragging(self):
        return self._middle_dragging.value

    @property
    def right_dragging(self):
        return self._right_dragging.value

    @property
    def begined_left_dragging(self):
        return self._left_dragging.changed and self._left_dragging.value

    @property
    def begined_middle_dragging(self):
        return self._middle_dragging.changed and self._middle_dragging.value

    @property
    def begined_right_dragging(self):
        return self._right_dragging.changed and self._right_dragging.value

    @property
    def left_down(self):
        return self._left_down.value

    @property
    def middle_down(self):
        return self._middle_down.value

    @property
    def right_down(self):
        return self._right_down.value

    @property
    def shift_down(self):
        return self._shift_down.value

    @property
    def ctrl_down(self):
        return self._ctrl_down.value

    @property
    def alt_down(self):
        return self._alt_down.value

    @property
    def changed_left_down(self) -> bool:
        return self._left_down.changed and self._left_down.value

    @property
    def changed_middle_down(self) -> bool:
        return self._middle_down.changed and self._middle_down.value

    @property
    def changed_right_down(self) -> bool:
        return self._right_down.changed and self._right_down.value

    @property
    def changed_left_up(self) -> bool:
        return self._left_down.changed and not self._left_down.value

    @property
    def changed_middle_up(self) -> bool:
        return self._middle_down.changed and not self._middle_down.value

    @property
    def changed_right_up(self) -> bool:
        return self._right_down.changed and not self._right_down.value

    @property
    def is_select_mode(self) -> bool:
        # Pressing the CTRL button switches to 'Multi-node selection mode'
        return self.ctrl_down

    @property
    def is_pan_mode(self) -> bool:
        # Pressing the ALT button switches to 'Canvas Pan Mode'
        return self.alt_down

    def as_unformatted_text(self):
        return (
            f"Pen: {self.pan_x:.02f}, {self.pan_y:.02f}\n"
            f"Zoom: {self.zoom:.02f}\n"
            f"Mouse pos: {self.mx:.02f}, {self.my:.02f}\n"
            f"Canvas pos: {self.cx:.02f}, {self.cy:.02f}\n"
            f"Canvas size: {self.cw:.02f}, {self.ch:.02f}\n"
            f"Activating: {self.activating}\n"
            f"Hovering: {self.hovering}\n"
            f"Left dragging: {self.left_dragging}\n"
            f"Middle dragging: {self.middle_dragging}\n"
            f"Right dragging: {self.right_dragging}\n"
            f"Left down: {self.left_down}\n"
            f"Middle down: {self.middle_down}\n"
            f"Right down: {self.right_down}\n"
            f"Ctrl down (Select): {self.ctrl_down}\n"
            f"Alt down (Pan): {self.alt_down}\n"
            f"Shift down: {self.shift_down}\n"
        )

    def drag_pan(self, dryrun=False):
        result = drag_float2(
            self._pan_label,
            self.pan_x,
            self.pan_y,
            self._pan_speed,
            self._pan_min,
            self._pan_max,
            self._pan_fmt,
            self._pan_flags,
        )
        if not dryrun and result:
            self.pan_x.value = result.value0
            self.pan_y.value = result.value1
        return result

    def slider_zoom(self, dryrun=False):
        result = slider_float(
            self._zoom_label,
            self.zoom,
            self._zoom_min,
            self._zoom_max,
            self._zoom_fmt,
            self._zoom_flags,
        )
        if not dryrun and result:
            self.zoom = result.value
        return result

    def input_local_pos(self):
        return input_float2(
            self._local_pos_label,
            self._local_pos_x,
            self._local_pos_y,
            self._local_pos_fmt,
            self._local_pos_flags,
        )

    def input_canvas_pos(self):
        return input_float2(
            self._canvas_pos_label,
            self._canvas_pos_x,
            self._canvas_pos_y,
            self._canvas_pos_fmt,
            self._canvas_pos_flags,
        )

    def tree_debugging(self) -> None:
        if imgui.tree_node("Debugging"):
            try:
                message = self.as_unformatted_text()
                imgui.text_unformatted(message.strip())
            finally:
                imgui.tree_pop()

    def render_controllers(self, dryrun=False, debugging=False) -> ControllerResult:
        pan = self.drag_pan(dryrun=dryrun)
        zoom = self.slider_zoom(dryrun=dryrun)

        with style_disable_input():
            self.input_local_pos()
            self.input_canvas_pos()

        if debugging:
            self.tree_debugging()

        changed = pan.clicked or zoom.changed
        return ControllerResult(changed, pan.value0, pan.value1, zoom.value)

    def point_in_canvas_rect(self, point: Point) -> bool:
        x, y = point
        cx, cy = self._canvas_pos
        cw, ch = self._canvas_size
        return cx <= x <= cx + cw and cy <= y <= cy + ch

    def canvas_to_screen_coords(self, point: Point) -> Point:
        x = self.cx + (point[0] + self.pan_x) * self.zoom
        y = self.cy + (point[1] + self.pan_y) * self.zoom
        return x, y

    def local_origin_to_screen_coords(self) -> Point:
        return self.canvas_to_screen_coords((0.0, 0.0))

    def mouse_to_screen_coords(self) -> Point:
        return self.canvas_to_screen_coords(self._mouse_pos)

    def canvas_to_screen_roi(self, roi: ROI) -> ROI:
        p1 = self.canvas_to_screen_coords((roi[0], roi[1]))
        p2 = self.canvas_to_screen_coords((roi[2], roi[3]))
        return p1[0], p1[1], p2[0], p2[1]

    def screen_to_canvas_coords(self, point: Point) -> Point:
        x = (point[0] - self.cx) / self.zoom - self.pan_x
        y = (point[1] - self.cy) / self.zoom - self.pan_y
        return x, y

    def mouse_to_canvas_coords(self) -> Point:
        return self.screen_to_canvas_coords(self._mouse_pos)

    @property
    def lock_threshold(self) -> float:
        """
        Pan (we use a zero mouse threshold when there's no context menu)
        You may decide to make that threshold dynamic based on whether
        the mouse is hovering something etc.
        """
        return self._lock_threshold if self._has_context_menu else 0.0

    def is_mouse_dragging(self, button: Union[int, MouseButton]) -> bool:
        if isinstance(button, MouseButton):
            button = int(button)
        assert isinstance(button, int)
        return imgui.is_mouse_dragging(button, self._lock_threshold)

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

    def update_state(self) -> ControllerResult:
        mx, my = imgui.get_mouse_pos()
        cx, cy = imgui.get_cursor_screen_pos()
        cw, ch = imgui.get_content_region_available()
        assert isinstance(mx, float)
        assert isinstance(my, float)
        assert isinstance(cx, float)
        assert isinstance(cy, float)
        assert isinstance(cw, float)
        assert isinstance(ch, float)
        self._draw_list = get_window_draw_list()
        self._mouse_pos = mx, my
        self._canvas_pos = cx, cy
        self._canvas_size = cw, ch

        # Using `imgui.invisible_button()` as a convenience
        # 1) it will advance the layout cursor and
        # 2) allows us to use `is_item_hovered()`/`is_item_active()`
        imgui.invisible_button(self._control_identifier, cw, ch, self._control_flags)

        self._activating.update(imgui.is_item_active())
        self._hovering.update(imgui.is_item_hovered())

        self._left_dragging.update(self.is_mouse_dragging(imgui.MOUSE_BUTTON_LEFT))
        self._middle_dragging.update(self.is_mouse_dragging(imgui.MOUSE_BUTTON_MIDDLE))
        self._right_dragging.update(self.is_mouse_dragging(imgui.MOUSE_BUTTON_RIGHT))

        io = imgui.get_io()
        self._left_down.update(bool(io.mouse_down[imgui.MOUSE_BUTTON_LEFT]))
        self._middle_down.update(bool(io.mouse_down[imgui.MOUSE_BUTTON_MIDDLE]))
        self._right_down.update(bool(io.mouse_down[imgui.MOUSE_BUTTON_RIGHT]))

        self._shift_down.update(io.key_shift)
        self._ctrl_down.update(io.key_ctrl)
        self._alt_down.update(io.key_alt)

        if self.activating:
            if self.middle_dragging:
                self.pan_x += io.mouse_delta.x / self.zoom
                self.pan_y += io.mouse_delta.y / self.zoom
            elif self.alt_down and self.left_dragging:
                self.pan_x += io.mouse_delta.x / self.zoom
                self.pan_y += io.mouse_delta.y / self.zoom

        if self.hovering and io.mouse_wheel != 0:
            if io.mouse_wheel > 0:
                self.zoom += self._zoom_step
            elif io.mouse_wheel < 0:
                self.zoom -= self._zoom_step

        if self.zoom > self._zoom_max:
            self.zoom = self._zoom_max
        elif self.zoom < self._zoom_min:
            self.zoom = self._zoom_min

        if self._hovering.value:
            mx, my = imgui.get_mouse_pos()
            assert isinstance(mx, float)
            assert isinstance(my, float)
            self._local_pos_x = mx - cx
            self._local_pos_y = my - cy

            scx, scy = self.screen_to_canvas_coords((mx, my))
            self._canvas_pos_x = scx
            self._canvas_pos_y = scy

        changed = self._pan_x.changed or self._pan_y.changed or self._zoom.changed
        return ControllerResult(changed, self.pan_x, self.pan_y, self.zoom)
