# -*- coding: utf-8 -*-

from typing import Final, Tuple

import imgui
from imgui.core import _DrawList  # noqa
from OpenGL import GL

from cvp.config.sections.av import AvSection
from cvp.types.override import override
from cvp.windows._window import Window

_WINDOW_NO_MOVE: Final[int] = imgui.WINDOW_NO_MOVE
_WINDOW_NO_SCROLLBAR: Final[int] = imgui.WINDOW_NO_SCROLLBAR
_WINDOW_NO_RESIZE: Final[int] = imgui.WINDOW_NO_RESIZE


class AvWindow(Window[AvSection]):
    def __init__(self, config: AvSection):
        super().__init__(config)

        self._flags = 0
        self._clear_color = 0.5, 0.5, 0.5, 1.0
        self._min_width = 400
        self._min_height = 300
        self._texture = 0
        self._popup_name = "ContextMenu"

    @override
    def on_create(self) -> None:
        assert self._texture == 0
        self._texture = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexImage2D(
            GL.GL_TEXTURE_2D,
            0,
            GL.GL_RGB,
            self._min_width,
            self._min_height,
            0,
            GL.GL_RGB,
            GL.GL_UNSIGNED_BYTE,
            None,
        )
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    @override
    def on_destroy(self) -> None:
        assert self._texture != 0
        GL.glDeleteTextures(1, self._texture)
        self._texture = 0

    @override
    def on_process(self) -> None:
        self._process_window()

    @property
    def window_title(self) -> str:
        name = self.config.name
        return name if name else type(self).__name__

    def _process_window(self) -> None:
        if not self.opened:
            return

        expanded, opened = imgui.begin(self.window_title, True, self._flags)
        try:
            if not opened:
                self.opened = False
                return

            if not expanded:
                return

            self._main()
        finally:
            imgui.end()

    def update_texture_size(self, size: Tuple[int, int]) -> None:
        if not self._texture:
            return

        width = size[0]
        height = size[1]
        if width <= 0 or height <= 0:
            return

        assert isinstance(width, int)
        assert isinstance(height, int)

        GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture)
        GL.glTexImage2D(
            GL.GL_TEXTURE_2D,
            0,
            GL.GL_RGB,
            width,
            height,
            0,
            GL.GL_RGB,
            GL.GL_UNSIGNED_BYTE,
            None,
        )
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    @staticmethod
    def begin_child_canvas() -> None:
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
        imgui.push_style_color(imgui.COLOR_CHILD_BACKGROUND, 0.5, 0.5, 0.5)
        child_flags = _WINDOW_NO_MOVE | _WINDOW_NO_SCROLLBAR | _WINDOW_NO_RESIZE
        space = imgui.get_style().item_spacing.y
        imgui.begin_child("Canvas", 0, -space, border=True, flags=child_flags)  # noqa
        imgui.pop_style_color()
        imgui.pop_style_var()

    def _main(self) -> None:
        if imgui.is_window_appearing():
            imgui.set_window_size(self._min_width, self._min_height)

        self.begin_child_canvas()
        try:
            self._child()
            self._popup()
        finally:
            imgui.end_child()

    def _child(self):
        cx, cy = imgui.get_cursor_screen_pos()
        cw, ch = imgui.get_content_region_available()

        draw_list = imgui.get_window_draw_list()
        assert isinstance(draw_list, _DrawList)

        filled_color = imgui.get_color_u32_rgba(*self._clear_color)
        draw_list.add_rect_filled(cx, cy, cx + cw, cy + cy, filled_color)

        w = int(cw)
        h = int(ch)
        size = w, h

        self.update_texture_size(size)

        p1 = cx, cy
        p2 = cx + cw, cy + ch
        draw_list.add_image(self._texture, p1, p2, (0, 0), (1, 1))

    @staticmethod
    def is_hovered_right_click():
        return (
            imgui.is_mouse_clicked(imgui.MOUSE_BUTTON_RIGHT)
            and imgui.is_window_hovered()
        )

    def _popup(self):
        if self.is_hovered_right_click():
            imgui.open_popup(self._popup_name)

        if imgui.begin_popup(self._popup_name):
            if imgui.menu_item("Option 1")[0]:
                print("Option 1 selected")
            if imgui.menu_item("Option 2")[0]:
                print("Option 2 selected")
            if imgui.menu_item("Option 3")[0]:
                print("Option 3 selected")
            imgui.end_popup()
