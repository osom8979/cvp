# -*- coding: utf-8 -*-

from typing import Optional

import imgui

from cvp.flow.datas import Canvas as CanvasProps
from cvp.imgui.draw_list import create_empty_draw_list, get_window_draw_list
from cvp.types.shapes import Point, Size
from cvp.widgets.canvas.controller import CanvasController


class BaseCanvas(CanvasController):
    _mouse_pos: Point
    _canvas_pos: Point
    _canvas_size: Size

    def __init__(self, canvas_props: Optional[CanvasProps] = None):
        super().__init__(canvas_props)
        self._mouse_pos = 0.0, 0.0
        self._canvas_pos = 0.0, 0.0
        self._canvas_size = 0.0, 0.0
        self._hovering = False
        self._left_button_clicked = False
        self._middle_button_clicked = False
        self._right_button_clicked = False
        self._draw_list = create_empty_draw_list()

    @property
    def mouse_pos(self):
        return self._mouse_pos

    @property
    def canvas_pos(self):
        return self._canvas_pos

    @property
    def canvas_size(self):
        return self._canvas_size

    @property
    def canvas_roi(self):
        return (
            self._canvas_pos[0],
            self._canvas_pos[1],
            self._canvas_pos[0] + self._canvas_size[0],
            self._canvas_pos[1] + self._canvas_size[1],
        )

    @property
    def draw_list(self):
        return self._draw_list

    def next_state(self):
        mx, my = imgui.get_mouse_pos()
        cx, cy = imgui.get_cursor_screen_pos()
        cw, ch = imgui.get_content_region_available()
        assert isinstance(mx, float)
        assert isinstance(my, float)
        assert isinstance(cx, float)
        assert isinstance(cy, float)
        assert isinstance(cw, float)
        assert isinstance(ch, float)
        self._mouse_pos = mx, my
        self._canvas_pos = cx, cy
        self._canvas_size = cw, ch
        self._hovering = cx <= mx <= cx + cw and cy <= my <= cy + ch
        self._left_button_clicked = imgui.is_mouse_clicked(imgui.MOUSE_BUTTON_LEFT)
        self._middle_button_clicked = imgui.is_mouse_clicked(imgui.MOUSE_BUTTON_MIDDLE)
        self._right_button_clicked = imgui.is_mouse_clicked(imgui.MOUSE_BUTTON_RIGHT)
        self._draw_list = get_window_draw_list()

    def do_button_control(self) -> None:
        self.do_control(self._canvas_pos, self._canvas_size)
