# -*- coding: utf-8 -*-

import os
from collections import OrderedDict
from io import StringIO
from typing import Optional, Tuple
from warnings import catch_warnings

import imgui
import pygame
from OpenGL import GL
from OpenGL.acceleratesupport import ACCELERATE_AVAILABLE
from OpenGL.error import Error

from cvp.config.sections.windows.media import MediaSection
from cvp.context import Context
from cvp.context.autofixer import AutoFixer
from cvp.logging.logging import logger
from cvp.popups.input_text import InputTextPopup
from cvp.popups.open_file import OpenFilePopup
from cvp.renderer.renderer import PygameRenderer
from cvp.widgets.fonts import add_jbm_font, add_ngc_font
from cvp.widgets.hoc.window import Window
from cvp.widgets.styles import default_style_colors
from cvp.windows.media import MediaWindow
from cvp.windows.medias import MediasWindow
from cvp.windows.overlay import OverlayWindow
from cvp.windows.preference import PreferenceWindow
from cvp.windows.processes import ProcessesWindow


class PlayerApplication:
    _renderer: PygameRenderer

    def __init__(self, context: Context):
        self._context = context
        self._windows = OrderedDict[str, Window]()

        self._overlay = OverlayWindow(self._context)
        self._medias = MediasWindow(self._context)
        self._processes = ProcessesWindow(self._context)
        self._preference = PreferenceWindow(self._context)

        self._open_file_popup = OpenFilePopup(title="Open file")
        self._open_url_popup = InputTextPopup(
            title="Open network stream",
            label="Please enter a network URL:",
            ok="Open",
            cancel="Close",
        )

    def add_windows(self, *windows: Window) -> None:
        for window in windows:
            self.add_window(window)

    def add_window(self, window: Window, key: Optional[str] = None) -> None:
        key = key if key else window.key
        assert isinstance(key, str)
        window.do_create()
        self._windows[key] = window

    def add_media_windows(self, *sections: MediaSection) -> None:
        for section in sections:
            self.add_media_window(section)

    def add_media_window(self, section: MediaSection) -> None:
        self.add_window(MediaWindow(self._context, section))

    @property
    def home(self):
        return self._context.home

    @property
    def config(self):
        return self._context.config

    @property
    def debug(self):
        return self._context.debug

    @property
    def verbose(self):
        return self._context.verbose

    def add_new_media_window(self, file: str) -> None:
        section = self.config.add_media_section()
        section.opened = True
        section.file = file
        section.name = file
        self.add_media_window(section)

    def _raise_force_egl_error(self, error: Error) -> None:
        fixer = AutoFixer[bool, Error](
            self._context,
            self.config.graphic,
            self.config.graphic.K.force_egl,
            True,
        )
        fixer.run(error)

    def start(self) -> None:
        self.on_init()
        try:
            self.on_process()
        except Error as e:
            if str(e) == "Attempt to retrieve context when no valid context":
                self._raise_force_egl_error(e)
            else:
                raise
        finally:
            self.on_exit()

    @property
    def pygame_display_size(self) -> Tuple[int, int]:
        assert pygame.display.get_init(), "pygame must be initialized"

        w = self.config.display.width
        h = self.config.display.height
        if w >= 1 and h >= 1:
            return w, h
        else:
            info = pygame.display.Info()
            return info.current_w, info.current_h

    @property
    def pygame_display_flags(self) -> int:
        common_flags = pygame.DOUBLEBUF | pygame.OPENGL
        if self.config.display.fullscreen:
            return common_flags | pygame.FULLSCREEN
        else:
            return common_flags | pygame.RESIZABLE

    def _validate_accelerate_available(self) -> None:
        if not self.config.graphic.has_use_accelerate:
            return

        use_accelerate = self.config.graphic.use_accelerate
        if use_accelerate != ACCELERATE_AVAILABLE:
            raise ValueError(
                f"The set 'use_accelerate' value ({use_accelerate}) "
                f"and 'accelerate_available' value ({ACCELERATE_AVAILABLE}) "
                "must be the same.\n"
                "Calling configuration and environment variables should take "
                "precedence over importing PyOpenGL."
            )

    def _raise_use_accelerate_error(self, error: ValueError) -> None:
        # 'numpy.dtype size changed, may indicate binary incompatibility.
        # Expected 96 from C header, got 88 from PyObject', 1,
        # <OpenGL.platform.baseplatform.glGenTextures object at 0x7b0a5ec96800>
        fixer = AutoFixer[bool, ValueError](
            self._context,
            self.config.graphic,
            self.config.graphic.K.use_accelerate,
            False,
        )
        fixer.run(error)

    def on_init(self) -> None:
        if self.debug:
            self._validate_accelerate_available()

        pygame.init()

        try:
            GL.glDeleteTextures(1, GL.glGenTextures(1))
        except ValueError as e:
            self._raise_use_accelerate_error(e)

        size = self.pygame_display_size
        flags = self.pygame_display_flags

        with catch_warnings(record=True) as wms:
            # [Warning]
            # PyGame seems to be running through X11 on top of wayland,
            # instead of wayland directly `pygame.display.set_mode(size, flags)`
            pygame.display.set_mode(size, flags)

            for wm in wms:
                buffer = StringIO()
                if self.verbose >= 1:
                    buffer.write(f"<{wm.category.__name__} ")
                    buffer.write(f"message='{str(wm.message)}' ")
                    buffer.write(f"file={wm.filename}:{wm.lineno}>")
                else:
                    buffer.write(f"{str(wm.message)}")
                logger.warning(buffer.getvalue())

        imgui.create_context()
        io = imgui.get_io()
        io.display_size = size
        io.ini_file_name = None
        io.log_file_name = None
        imgui.load_ini_settings_from_disk(str(self.home.gui_ini))

        self._renderer = PygameRenderer()

        io.fonts.clear()
        pixels = self.config.font.pixels
        scale = self.config.font.scale
        font_size_pixels = pixels * scale
        add_jbm_font(font_size_pixels)
        add_ngc_font(font_size_pixels)

        user_font = self.config.font.family
        if user_font and os.path.isfile(user_font):
            korean_ranges = io.fonts.get_glyph_ranges_korean()
            io.fonts.add_font_from_file_ttf(user_font, font_size_pixels, korean_ranges)

        io.font_global_scale /= self.config.font.scale
        self._renderer.refresh_font_texture()

        theme = self.config.appearance.theme
        default_style_colors(theme)

        GL.glClearColor(0, 0, 0, 1)

        self.add_windows(
            self._overlay,
            self._medias,
            self._processes,
            self._preference,
        )
        self.add_media_windows(*self.config.media_sections.values())

    def on_exit(self) -> None:
        self._context.teardown()

        while self._windows:
            key, win = self._windows.popitem(last=False)
            win.do_destroy()

        if not self._context.readonly:
            self.config.display.fullscreen = pygame.display.is_fullscreen()
            self.config.display.size = pygame.display.get_window_size()
            self._context.save_config()
            imgui.save_ini_settings_to_disk(str(self.home.gui_ini))

        del self._renderer
        pygame.quit()

    def on_process(self) -> None:
        while not self._context.is_done():
            self.on_event()
            self.on_frame()

    def on_event(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._context.quit()
            self._renderer.do_event(event)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] and keys[pygame.K_q]:
            self._context.quit()
        if keys[pygame.K_LCTRL] and keys[pygame.K_o]:
            self._open_file_popup.show()
        if keys[pygame.K_LCTRL] and keys[pygame.K_n]:
            self._open_url_popup.show()

        if keys[pygame.K_LCTRL] and keys[pygame.K_LALT] and keys[pygame.K_m]:
            self._medias.opened = True
        if keys[pygame.K_LCTRL] and keys[pygame.K_LALT] and keys[pygame.K_p]:
            self._processes.opened = True
        if keys[pygame.K_LCTRL] and keys[pygame.K_LALT] and keys[pygame.K_s]:
            self._preference.opened = True

        self._renderer.do_tick()

    def on_frame(self) -> None:
        imgui.new_frame()
        try:
            GL.glClear(GL.GL_COLOR_BUFFER_BIT)
            self.on_main_menu()
            self.on_popups()
            for win in self._windows.values():
                win.do_process()
            self.on_demo_window()
        finally:
            # Cannot use `screen.fill((1, 1, 1))` because pygame's screen does not
            # support fill() on OpenGL surfaces
            imgui.render()
            self._renderer.render(imgui.get_draw_data())
            pygame.display.flip()

    def on_main_menu(self) -> None:
        with imgui.begin_main_menu_bar():
            if imgui.begin_menu("File"):
                if imgui.menu_item("Open file", "Ctrl+O")[0]:
                    self._open_file_popup.show()
                if imgui.menu_item("Open network", "Ctrl+N")[0]:
                    self._open_url_popup.show()

                imgui.separator()
                _manager_opened = self._medias.opened
                _processes_opened = self._processes.opened
                _preference_opened = self._preference.opened

                if imgui.menu_item("Medias", "Ctrl+Alt+M", _manager_opened)[0]:
                    self._medias.opened = not self._medias.opened
                if imgui.menu_item("Processes", "Ctrl+Alt+P", _processes_opened)[0]:
                    self._processes.opened = not self._processes.opened
                if imgui.menu_item("Preference", "Ctrl+Alt+S", _preference_opened)[0]:
                    self._preference.opened = not self._preference.opened

                imgui.separator()
                if imgui.menu_item("Quit", "Ctrl+Q")[0]:
                    self._context.quit()
                imgui.end_menu()

            if imgui.begin_menu("Windows"):
                for key, win in self._windows.items():
                    if imgui.menu_item(key, None, win.opened)[0]:
                        win.opened = not win.opened
                if self.debug:
                    imgui.separator()
                    if imgui.menu_item("Demo", None, self.config.demo.opened)[0]:
                        self.config.demo.opened = not self.config.demo.opened
                imgui.end_menu()

    def on_popups(self) -> None:
        file = self._open_file_popup.do_process()
        if file:
            self.add_new_media_window(file)

        url = self._open_url_popup.do_process()
        if url:
            self.add_new_media_window(url)

    def on_demo_window(self) -> None:
        if not self.debug:
            return
        if not self.config.demo.opened:
            return
        imgui.show_test_window()
