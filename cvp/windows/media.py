# -*- coding: utf-8 -*-

from ctypes import addressof, c_void_p, create_string_buffer, memmove
from typing import Final

import imgui
from imgui.core import _DrawList  # noqa
from OpenGL import GL

from cvp.config.sections.windows.media import MediaSection
from cvp.context import Context
from cvp.types import override
from cvp.widgets import menu_item_ex
from cvp.widgets.hoc.window import Window

_WINDOW_NO_MOVE: Final[int] = imgui.WINDOW_NO_MOVE
_WINDOW_NO_SCROLLBAR: Final[int] = imgui.WINDOW_NO_SCROLLBAR
_WINDOW_NO_RESIZE: Final[int] = imgui.WINDOW_NO_RESIZE


class MediaWindow(Window[MediaSection]):
    def __init__(self, context: Context, section: MediaSection):
        super().__init__(
            context=context,
            section=section,
            title="Media",
            closable=True,
            flags=None,
            use_config_title=True,
        )

        self._clear_color = 0.5, 0.5, 0.5, 1.0
        self._texture = 0
        self._pbo = 0
        self._prev_frame_index = 0

    @override
    def on_create(self) -> None:
        assert self._texture == 0
        assert self._pbo == 0

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

        self._pbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_PIXEL_UNPACK_BUFFER, self._pbo)
        size = self._min_width * self._min_height * 3
        GL.glBufferData(GL.GL_PIXEL_UNPACK_BUFFER, size, None, GL.GL_STREAM_DRAW)
        GL.glBindBuffer(GL.GL_PIXEL_UNPACK_BUFFER, 0)

        assert self._texture != 0
        assert self._pbo != 0

    @override
    def on_destroy(self) -> None:
        assert self._texture != 0
        assert self._pbo != 0

        GL.glDeleteTextures(1, self._texture)
        self._texture = 0

        GL.glDeleteBuffers(1, self._pbo)
        self._pbo = 0

    @override
    def on_process(self) -> None:
        self.begin_child_canvas()
        try:
            self._child()
            self._popup()
        finally:
            imgui.end_child()

    def update_texture(self) -> None:
        if not self._texture:
            return

        process = self.context.pm.get(self.section.section)
        if process is None:
            return

        if process.poll() is not None:
            return

        pixels = process.dequeue_latest()
        if not pixels:
            return

        if self._prev_frame_index == process.latest_count:
            return

        self._prev_frame_index = process.latest_count
        width = process.frame_shape.width
        height = process.frame_shape.height
        channels = process.frame_shape.channels

        if width <= 0 or height <= 0:
            return

        assert isinstance(width, int)
        assert isinstance(height, int)
        assert isinstance(channels, int)
        assert channels == 3

        self.update_texture_image_2d(width, height, pixels)
        # self.update_texture_with_pbo(width, height, channels, pixels)

    def update_texture_image_2d(self, width: int, height: int, pixels: bytes) -> None:
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
            pixels,
        )
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    def update_texture_with_pbo(
        self,
        width: int,
        height: int,
        channels: int,
        pixels: bytes,
    ) -> None:
        GL.glBindBuffer(GL.GL_PIXEL_UNPACK_BUFFER, self._pbo)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture)
        GL.glTexSubImage2D(
            GL.GL_TEXTURE_2D,
            0,
            0,
            0,
            width,
            height,
            GL.GL_RGB,
            GL.GL_UNSIGNED_BYTE,
            c_void_p(0),
        )

        size = width * height * channels

        GL.glBindBuffer(GL.GL_PIXEL_UNPACK_BUFFER, self._pbo)
        GL.glBufferData(GL.GL_PIXEL_UNPACK_BUFFER, size, None, GL.GL_STREAM_DRAW)

        buffer_ptr = GL.glMapBuffer(GL.GL_PIXEL_UNPACK_BUFFER, GL.GL_WRITE_ONLY)
        if buffer_ptr:
            pixels_ptr = addressof(create_string_buffer(pixels, size))
            memmove(buffer_ptr, pixels_ptr, size)
            GL.glUnmapBuffer(GL.GL_PIXEL_UNPACK_BUFFER)

        GL.glBindBuffer(GL.GL_PIXEL_UNPACK_BUFFER, 0)

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

        self.update_texture()

        p1 = cx, cy
        p2 = cx + cw, cy + ch
        draw_list.add_image(self._texture, p1, p2, (0, 0), (1, 1))

    def _popup(self):
        if imgui.begin_popup_context_window():
            if menu_item_ex("Option 1"):
                print("Option 1 selected")
            if menu_item_ex("Option 2"):
                print("Option 2 selected")
            if menu_item_ex("Option 3"):
                print("Option 3 selected")
            imgui.end_popup()
