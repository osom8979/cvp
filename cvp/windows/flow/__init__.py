# -*- coding: utf-8 -*-

from typing import Final

import imgui
from imgui.core import _DrawList  # noqa

from cvp.config.sections.windows.flow import FlowSection
from cvp.context import Context
from cvp.types import override
from cvp.widgets import menu_item_ex
from cvp.widgets.hoc.window import Window

_WINDOW_NO_MOVE: Final[int] = imgui.WINDOW_NO_MOVE
_WINDOW_NO_SCROLLBAR: Final[int] = imgui.WINDOW_NO_SCROLLBAR
_WINDOW_NO_RESIZE: Final[int] = imgui.WINDOW_NO_RESIZE


class FlowWindow(Window[FlowSection]):
    def __init__(self, context: Context, section: FlowSection):
        super().__init__(
            context=context,
            section=section,
            title="Flow",
            closable=True,
            flags=None,
        )

        self._clear_color = 0.5, 0.5, 0.5, 1.0
        self._texture = 0
        self._pbo = 0
        self._prev_frame_index = 0

    @override
    def on_create(self) -> None:
        pass

    @override
    def on_destroy(self) -> None:
        pass

    @override
    def on_process(self) -> None:
        self.begin_child_canvas()
        try:
            self._child()
            self._popup()
        finally:
            imgui.end_child()

    @staticmethod
    def begin_child_canvas() -> None:
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
        imgui.push_style_color(imgui.COLOR_CHILD_BACKGROUND, 0.5, 0.5, 0.5)
        child_flags = _WINDOW_NO_MOVE | _WINDOW_NO_SCROLLBAR | _WINDOW_NO_RESIZE
        space = imgui.get_style().item_spacing.y
        imgui.begin_child("Canvas", 0, -space, border=True, flags=child_flags)  # noqa
        imgui.pop_style_color()
        imgui.pop_style_var()

    def _child(self):
        cx, cy = imgui.get_cursor_screen_pos()
        cw, ch = imgui.get_content_region_available()

        draw_list = imgui.get_window_draw_list()
        assert isinstance(draw_list, _DrawList)

        filled_color = imgui.get_color_u32_rgba(*self._clear_color)
        draw_list.add_rect_filled(cx, cy, cx + cw, cy + cy, filled_color)

        # p1 = cx, cy
        # p2 = cx + cw, cy + ch

    def _popup(self):
        if imgui.begin_popup_context_window():
            if menu_item_ex("Option 1"):
                print("Option 1 selected")
            if menu_item_ex("Option 2"):
                print("Option 2 selected")
            if menu_item_ex("Option 3"):
                print("Option 3 selected")
            imgui.end_popup()
