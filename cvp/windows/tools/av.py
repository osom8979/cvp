# -*- coding: utf-8 -*-

import os
from typing import Optional, Tuple

import imgui
from imgui.core import _DrawList  # noqa
from mpv import MPV, MpvGlGetProcAddressFn, MpvRenderContext
from OpenGL import GL

from cvp.config.sections.tools import ToolsSection
from cvp.logging.logging import DEBUG, convert_level_number, logger, mpv_logger
from cvp.renderer.gl import get_process_address
from cvp.types.override import override
from cvp.widgets.popups.open_file import OpenFilePopup
from cvp.windows._window import Window


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


OPENGL_INIT_PARAMS = dict(get_proc_address=MpvGlGetProcAddressFn(_get_process_address))


class AvWindow(Window):
    _file: Optional[str]
    _fbo: Optional[int]
    _texture: Optional[int]
    _mpv: Optional[MPV]
    _context: Optional[MpvRenderContext]

    def __init__(self, config: ToolsSection, flags=imgui.WINDOW_MENU_BAR):
        self._config = config
        self._flags = flags
        self._popup = OpenFilePopup()
        self._clear_color = 0.5, 0.5, 0.5, 1.0
        self._pos = 0.0
        self._volume = 0.0
        self._min_width = 400
        self._min_height = 300

        self._open = None
        self._file = None
        self._fbo = None
        self._texture = None
        self._mpv = None
        self._context = None

    def open(self, file: str) -> None:
        if not os.path.isfile(file):
            return

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

        self._mpv = MPV(log_handler=_logging_handler, loglevel="debug")
        self._context = MpvRenderContext(
            mpv=self._mpv,
            api_type="opengl",
            opengl_init_params=OPENGL_INIT_PARAMS,
        )

        self._mpv.play(file)
        self._mpv.volume = 0
        self._file = file

    def close(self) -> None:
        if self._context:
            self._context.free()
        if self._mpv:
            self._mpv.terminate()

        # GL.glDeleteTextures(1, self._texture)
        # GL.glDeleteFramebuffers(1, self._fbo)

        self._open = None
        self._file = None
        self._fbo = None
        self._texture = None
        self._mpv = None
        self._context = None

    def _on_file_open(self, file: Optional[str]) -> None:
        if not file:
            return
        self.open(file)

    def open_file_popup(self) -> None:
        self._popup.show(title="Open video file", callback=self._on_file_open)

    @staticmethod
    def slider(label: str, value: float) -> Tuple[bool, float]:
        changed, value = imgui.slider_float(
            f"##{label}", value, 0.0, 100.0, f"{label} %.0f", 1.0
        )
        assert isinstance(changed, bool)
        assert isinstance(value, float)
        return changed, value

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

        changed, value = self.slider("Playback Percentage", self._pos)
        if self._mpv is not None:
            if changed:
                try:
                    self._mpv.command("seek", value, "absolute-percent")
                except BaseException as e:
                    logger.exception(e)
                else:
                    self._pos = value
            else:
                self._pos = self._mpv.percent_pos

        changed, value = self.slider("Volume Percentage", self._volume)
        if self._mpv is not None:
            if changed:
                try:
                    self._mpv.volume = value
                except BaseException as e:
                    logger.exception(e)
                else:
                    self._volume = value
            else:
                self._volume = self._mpv.volume

        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
        imgui.push_style_color(imgui.COLOR_CHILD_BACKGROUND, 0.5, 0.5, 0.5)
        child_flags = (
            imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_RESIZE
        )
        space = imgui.get_style().item_spacing.y
        imgui.begin_child("Canvas", 0, -space, border=True, flags=child_flags)  # noqa
        imgui.pop_style_color()
        imgui.pop_style_var()

        try:
            canvas_pos = imgui.get_cursor_screen_pos()
            canvas_size = imgui.get_content_region_available()
            cx, cy = canvas_pos
            cw, ch = canvas_size

            draw_list = imgui.get_window_draw_list()
            assert isinstance(draw_list, _DrawList)

            filled_color = imgui.get_color_u32_rgba(*self._clear_color)
            draw_list.add_rect_filled(cx, cy, cx + cw, cy + cy, filled_color)

            w = int(cw)
            h = int(ch)

            if self._context and self._context.update() and w > 0 and h > 0:
                GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self._fbo)
                GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture)

                GL.glTexImage2D(
                    GL.GL_TEXTURE_2D,
                    0,
                    GL.GL_RGB,
                    w,
                    h,
                    0,
                    GL.GL_RGB,
                    GL.GL_UNSIGNED_BYTE,
                    None,
                )

                GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
                GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

                self._context.render(
                    flip_y=False,
                    opengl_fbo=dict(w=w, h=h, fbo=self._fbo),
                )

                p1 = cx, cy
                p2 = cx + cw, cy + ch
                img_color = imgui.get_color_u32_rgba(1.0, 1.0, 1.0, 1.0)
                draw_list.add_image(self._texture, p1, p2, (0, 0), (1, 1), img_color)
                # imgui.image(self._texture, w, h)
        finally:
            imgui.end_child()

    def _process_window(self) -> None:
        if not self._config.av:
            return

        expanded, opened = imgui.begin("AvWindow", True, self._flags)
        try:
            if not opened:
                self._config.av = False
                return

            if not expanded:
                return

            self._main()
        finally:
            imgui.end()

    @override
    def on_create(self) -> None:
        pass

    @override
    def on_destroy(self) -> None:
        pass

    @override
    def on_process(self) -> None:
        self._process_window()
        self._popup.process()
