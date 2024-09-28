# -*- coding: utf-8 -*-

from typing import Final

import imgui

from cvp.config.sections.flow_window import FlowWindowSection
from cvp.context import Context
from cvp.gui.begin_child import begin_child
from cvp.gui.draw_list import get_window_draw_list
from cvp.gui.menu_item_ex import menu_item_ex
from cvp.types import override
from cvp.widgets.canvas_control import CanvasControl
from cvp.widgets.cutting_edge import CuttingEdge
from cvp.windows.flow.tabs import Tabs

_WINDOW_NO_MOVE: Final[int] = imgui.WINDOW_NO_MOVE
_WINDOW_NO_SCROLLBAR: Final[int] = imgui.WINDOW_NO_SCROLLBAR
_WINDOW_NO_RESIZE: Final[int] = imgui.WINDOW_NO_RESIZE
CANVAS_FLAGS: Final[int] = _WINDOW_NO_MOVE | _WINDOW_NO_SCROLLBAR | _WINDOW_NO_RESIZE


class FlowWindow(CuttingEdge[FlowWindowSection]):
    def __init__(self, context: Context):
        super().__init__(
            context=context,
            section=context.config.flow_window,
            title="Flow",
            closable=True,
        )
        self._tabs = Tabs(context)
        self._control = CanvasControl()
        self._grid_step = 50.0
        self._draw_grid = True
        self._clear_color = 0.5, 0.5, 0.5, 1.0
        self._grid_filled_color = 0.5, 0.5, 0.5, 1.0
        self._grid_line_color = 0.8, 0.8, 0.8, 0.2
        self._background = None
        self._enable_context_menu = True

    @override
    def on_process_sidebar_right(self):
        self._control.on_process()
        self._tabs.do_process()

    @override
    def on_process_main(self) -> None:
        self.begin_child_canvas()
        try:
            self.on_canvas()
            self.on_popup_menu()
        finally:
            imgui.end_child()

    @staticmethod
    def begin_child_canvas() -> None:
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
        imgui.push_style_color(imgui.COLOR_CHILD_BACKGROUND, 0.5, 0.5, 0.5)
        try:
            return begin_child("## Canvas", border=True, flags=CANVAS_FLAGS)
        finally:
            imgui.pop_style_color()
            imgui.pop_style_var()

    def on_canvas(self):
        cx, cy = imgui.get_cursor_screen_pos()
        cw, ch = imgui.get_content_region_available()
        assert isinstance(cx, float)
        assert isinstance(cy, float)
        assert isinstance(cw, float)
        assert isinstance(ch, float)
        canvas_pos = cx, cy
        canvas_size = cw, ch

        draw_list = get_window_draw_list()
        filled_color = imgui.get_color_u32_rgba(*self._clear_color)
        draw_list.add_rect_filled(cx, cy, cx + cw, cy + cy, filled_color)

        self._control.do_control(
            canvas_size=canvas_size,
            has_context_menu=self._enable_context_menu,
        )

        if self._draw_grid:
            grid_color = imgui.get_color_u32_rgba(*self._grid_line_color)
            step = self._grid_step
            thickness = 1.0
            for line in self._control.vertical_lines(step, canvas_pos, canvas_size):
                x1, y1, x2, y2 = line
                draw_list.add_line(x1, y1, x2, y2, grid_color, thickness)
            for line in self._control.horizontal_lines(step, canvas_pos, canvas_size):
                x1, y1, x2, y2 = line
                draw_list.add_line(x1, y1, x2, y2, grid_color, thickness)

        if self._background is not None:
            img_id = self._background.texture_id
            img_x = 0
            img_y = 0
            img_w = self._background.width
            img_h = self._background.height
            img_roi = img_x, img_y, img_w, img_h
            img_p1, img_p2 = self._control.calc_roi(img_roi, canvas_pos)

            alpha = self._control.alpha
            img_color = imgui.get_color_u32_rgba(1.0, 1.0, 1.0, alpha)
            draw_list.add_image(img_id, img_p1, img_p2, (0, 0), (1, 1), img_color)

    def on_popup_menu(self):
        if not self._enable_context_menu:
            return

        if not imgui.begin_popup_context_window().opened:
            return

        try:
            if menu_item_ex("Reset"):
                self._control.reset()
        finally:
            imgui.end_popup()
