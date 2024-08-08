# -*- coding: utf-8 -*-

import os
from typing import Final, Optional, Tuple

import imgui
from imgui.core import _DrawList  # noqa
from mpv import MPV, MpvGlGetProcAddressFn, MpvRenderContext
from OpenGL import GL

from cvp.config.sections.mpv import MpvSection
from cvp.logging.logging import DEBUG, convert_level_number, logger, mpv_logger
from cvp.renderer.gl import get_process_address
from cvp.types.override import override
from cvp.widgets.popups.open_file import OpenFilePopup
from cvp.windows._window import Window

_WINDOW_NO_MOVE: Final[int] = imgui.WINDOW_NO_MOVE
_WINDOW_NO_SCROLLBAR: Final[int] = imgui.WINDOW_NO_SCROLLBAR
_WINDOW_NO_RESIZE: Final[int] = imgui.WINDOW_NO_RESIZE


def _get_process_address(ctx, name: bytes) -> int:
    func_name = str(name, encoding="utf-8")
    addr = get_process_address(func_name)
    addr = addr if addr is not None else 0
    assert isinstance(addr, int)
    mpv_logger.debug(f"get_process_address(ctx={ctx}, name={func_name}) -> {addr}")
    return addr


def _convert_level_number(level: str) -> int:
    if level == "v":
        return DEBUG

    try:
        return convert_level_number(level)
    except BaseException as e:
        mpv_logger.warning(e)
        return DEBUG


def _logging_handler(level: str, prefix: str, text: str) -> None:
    assert isinstance(level, str)
    assert isinstance(prefix, str)
    assert isinstance(text, str)
    log_level = _convert_level_number(level)
    mpv_logger.log(log_level, f"[{prefix}] {text.strip()}")


class MpvWindow(Window[MpvSection]):
    _file: Optional[str]
    _mpv: Optional[MPV]
    _context: Optional[MpvRenderContext]

    def __init__(self, config: MpvSection, flags=imgui.WINDOW_MENU_BAR):
        super().__init__(config)

        self._flags = flags
        self._popup = OpenFilePopup()
        self._clear_color = 0.5, 0.5, 0.5, 1.0
        self._playback = 0.0
        self._volume = 0.0
        self._min_width = 400
        self._min_height = 300

        self._fbo = 0
        self._texture = 0

        self._file = None
        self._mpv = None
        self._context = None

    @override
    def on_create(self) -> None:
        self._fbo = GL.glGenFramebuffers(1)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self._fbo)

        self._texture = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture)

        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)

        GL.glFramebufferTexture2D(
            GL.GL_FRAMEBUFFER,
            GL.GL_COLOR_ATTACHMENT0,
            GL.GL_TEXTURE_2D,
            self._texture,
            0,
        )

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
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)

    @override
    def on_destroy(self) -> None:
        if self._texture:
            GL.glDeleteTextures(1, self._texture)
        if self._fbo:
            GL.glDeleteFramebuffers(1, self._fbo)

        self._texture = 0
        self._fbo = 0

    @override
    def on_process(self) -> None:
        self._process_window()
        self._popup.process()

    def _process_window(self) -> None:
        if not self.opened:
            return

        expanded, opened = imgui.begin(type(self).__name__, True, self._flags)
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

    def open(self, file: str) -> None:
        if not os.path.isfile(file):
            return

        self._mpv = MPV(log_handler=_logging_handler, loglevel="debug")
        self._context = MpvRenderContext(
            mpv=self._mpv,
            api_type="opengl",
            opengl_init_params={
                "get_proc_address": MpvGlGetProcAddressFn(_get_process_address),
            },
        )
        self._mpv.play(file)
        self._mpv.volume = self._volume
        self._file = file

    def close(self) -> None:
        if self._context:
            self._context.free()
        if self._mpv:
            self._mpv.terminate()

        self._file = None
        self._mpv = None
        self._context = None

    @property
    def context_opened(self) -> bool:
        if self._context is not None:
            assert self._file is not None
            assert self._mpv is not None
            assert self._context is not None
            return True
        else:
            assert self._file is None
            assert self._mpv is None
            assert self._context is None
            return False

    def render(self, size: Tuple[int, int]) -> None:
        if not self._context:
            return
        if not self._fbo:
            return
        if not self._context.update():
            return

        width = size[0]
        height = size[1]
        if width <= 0 or height <= 0:
            return

        assert isinstance(width, int)
        assert isinstance(height, int)

        self._context.render(
            flip_y=False,
            opengl_fbo=dict(w=width, h=height, fbo=self._fbo),
        )

    def on_open_file(self, file: Optional[str]) -> None:
        if not file:
            return
        self.open(file)

    def open_file_popup(self) -> None:
        self._popup.show(
            title="Open video file",
            callback=self.on_open_file,
        )

    @staticmethod
    def slider_float(label: str, value: float) -> Tuple[bool, float]:
        changed, value = imgui.slider_float(
            f"## {label}", value, 0.0, 100.0, f"{label} %.0f", 1.0
        )
        assert isinstance(changed, bool)
        assert isinstance(value, float)
        return changed, value

    @staticmethod
    def begin_child_canvas() -> None:
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
        imgui.push_style_color(imgui.COLOR_CHILD_BACKGROUND, 0.5, 0.5, 0.5)
        child_flags = _WINDOW_NO_MOVE | _WINDOW_NO_SCROLLBAR | _WINDOW_NO_RESIZE
        space = imgui.get_style().item_spacing.y
        imgui.begin_child("Canvas", 0, -space, border=True, flags=child_flags)  # noqa
        imgui.pop_style_color()
        imgui.pop_style_var()

    def slider_playback(self) -> None:
        changed, value = self.slider_float("Playback Percentage", self._playback)
        if self._mpv is not None:
            if changed:
                try:
                    self._mpv.command("seek", value, "absolute-percent")
                except BaseException as e:
                    logger.exception(e)
                else:
                    self._playback = value
            elif self._mpv.percent_pos is not None:
                self._playback = self._mpv.percent_pos

    def slider_volume(self) -> None:
        changed, value = self.slider_float("Volume Percentage", self._volume)
        if self._mpv is not None:
            if changed:
                try:
                    self._mpv.volume = value
                except BaseException as e:
                    logger.exception(e)
                else:
                    self._volume = value
            elif self._mpv.volume is not None:
                self._volume = self._mpv.volume

    def _main(self) -> None:
        if imgui.is_window_appearing():
            imgui.set_window_size(self._min_width, self._min_height)

        if imgui.begin_menu_bar().opened:
            if imgui.begin_menu("File").opened:
                if imgui.menu_item("Open")[0]:
                    self.open_file_popup()

                imgui.separator()
                if imgui.menu_item("Close")[0]:
                    self.close()
                imgui.end_menu()
            imgui.end_menu_bar()

        imgui.push_item_width(-1)
        self.slider_playback()
        self.slider_volume()
        imgui.pop_item_width()

        self.begin_child_canvas()
        try:
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
            self.render(size)

            if self.context_opened:
                p1 = cx, cy
                p2 = cx + cw, cy + ch
                draw_list.add_image(self._texture, p1, p2, (0, 0), (1, 1))
        finally:
            imgui.end_child()
