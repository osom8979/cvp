# -*- coding: utf-8 -*-

from typing import Final

import imgui

from cvp.config.sections.windows.manager.labeling import LabelingManagerSection
from cvp.context import Context
from cvp.types import override
from cvp.widgets import get_window_draw_list
from cvp.widgets.hoc.sidebar_with_main import SidebarWithMain

WINDOW_NO_MOVE: Final[int] = imgui.WINDOW_NO_MOVE
WINDOW_NO_SCROLLBAR: Final[int] = imgui.WINDOW_NO_SCROLLBAR
WINDOW_NO_RESIZE: Final[int] = imgui.WINDOW_NO_RESIZE


class LabelingWindow(SidebarWithMain[LabelingManagerSection]):
    def __init__(self, context: Context):
        super().__init__(
            context=context,
            section=context.config.labeling_manager,
            title="Labeling",
            closable=True,
        )
        self._clear_color = 0.5, 0.5, 0.5, 1.0

    @override
    def on_process_sidebar(self):
        pass

    @override
    def on_process_main(self) -> None:
        self.begin_child_canvas()
        try:
            self.on_canvas()
        finally:
            imgui.end_child()

    @staticmethod
    def begin_child_canvas() -> None:
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
        imgui.push_style_color(imgui.COLOR_CHILD_BACKGROUND, 0.5, 0.5, 0.5)
        canvas_flags = WINDOW_NO_MOVE | WINDOW_NO_SCROLLBAR | WINDOW_NO_RESIZE
        space = imgui.get_style().item_spacing.y
        imgui.begin_child("Canvas", 0, -space, border=True, flags=canvas_flags)  # noqa
        imgui.pop_style_color()
        imgui.pop_style_var()

    def on_canvas(self):
        cx, cy = imgui.get_cursor_screen_pos()
        cw, ch = imgui.get_content_region_available()

        draw_list = get_window_draw_list()
        filled_color = imgui.get_color_u32_rgba(*self._clear_color)
        draw_list.add_rect_filled(cx, cy, cx + cw, cy + cy, filled_color)