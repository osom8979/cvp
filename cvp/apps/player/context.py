# -*- coding: utf-8 -*-

import os
from argparse import Namespace
from pathlib import Path
from typing import Dict, Optional, Tuple

import imgui
import pygame
from OpenGL import GL
from OpenGL.error import Error

from cvp.arguments import CVP_HOME, IMGUI_INI_FILENAME, PLAYER_INI_FILENAME
from cvp.assets import get_default_font_path
from cvp.config.config import Config
from cvp.config.sections.display import force_egl_section_key
from cvp.filesystem.permission import test_directory, test_readable
from cvp.logging.logging import logger
from cvp.renderer.renderer import PygameRenderer
from cvp.widgets.popups.open_file import OpenFilePopup
from cvp.widgets.popups.open_url import OpenUrlPopup

# noinspection PyProtectedMember
from cvp.windows._window import Window
from cvp.windows.av import AvWindow
from cvp.windows.mpv import MpvWindow
from cvp.windows.overlay import OverlayWindow
from cvp.windows.preference import PreferenceWindow


class PlayerContext:
    _renderer: PygameRenderer
    _windows: Dict[str, Window]

    def __init__(
        self,
        home: Optional[str] = None,
        debug=False,
        verbose=0,
    ):
        self._home = Path(home) if home else CVP_HOME
        self._imgui_ini = self._home / IMGUI_INI_FILENAME
        self._player_ini = self._home / PLAYER_INI_FILENAME
        self._debug = debug
        self._verbose = verbose

        if not self._home.exists():
            self._home.mkdir(parents=True, exist_ok=True)

        test_directory(self._home)
        test_readable(self._home)

        self._readonly = not os.access(self._home, os.W_OK)
        self._config = Config(self._player_ini)
        self._done = False
        self._windows = {
            "__overlay__": OverlayWindow(self._config.overlay),
            "__mpv__": MpvWindow(self._config.mpv),
        }
        self._preference = PreferenceWindow(self._config)
        for av_config in self._config.avs:
            self._windows[av_config.section] = AvWindow(av_config)

        self._open_file_popup = OpenFilePopup()
        self._open_url_popup = OpenUrlPopup()

    @classmethod
    def from_namespace(cls, args: Namespace):
        assert isinstance(args.home, str)
        assert isinstance(args.debug, bool)
        assert isinstance(args.verbose, int)
        return cls(
            home=args.home,
            debug=args.debug,
            verbose=args.verbose,
        )

    def quit(self):
        self._done = True

    def add_av_window(self, file: str) -> None:
        section = self._config.add_av_section()
        section.opened = True
        section.file = file
        section.name = file

        window = AvWindow(section)
        window.do_create()

        self._windows[section.section] = window

    def on_open_file(self, file: Optional[str]) -> None:
        if not file:
            return
        self.add_av_window(file)

    def open_file(self):
        self._open_file_popup.show(
            title="Open file",
            callback=self.on_open_file,
        )

    def on_open_url(self, file: Optional[str]) -> None:
        if not file:
            return
        self.add_av_window(file)

    def open_url(self):
        self._open_url_popup.show(
            title="Open network stream",
            callback=self.on_open_url,
        )

    def start(self) -> None:
        self.on_init()
        try:
            self.on_process()
        except Error as e:
            if str(e) == "Attempt to retrieve context when no valid context":
                section, key = force_egl_section_key()
                logger.error(
                    f"Please modify the value of '{key}' to 'True' in the '[{section}]'"
                    f" section of the '{str(self._player_ini)}' file and try again."
                )
                raise RuntimeError("Consider enabling EGL related options") from e
        finally:
            self.on_exit()

    @property
    def pygame_display_size(self) -> Tuple[int, int]:
        assert pygame.display.get_init(), "pygame must be initialized"

        w = self._config.display.width
        h = self._config.display.height
        if w >= 1 and h >= 1:
            return w, h
        else:
            info = pygame.display.Info()
            return info.current_w, info.current_h

    @property
    def pygame_display_flags(self) -> int:
        common_flags = pygame.DOUBLEBUF | pygame.OPENGL
        if self._config.display.fullscreen:
            return common_flags | pygame.FULLSCREEN
        else:
            return common_flags | pygame.RESIZABLE

    def on_init(self) -> None:
        if self._config.display.force_egl:
            os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"

        pygame.init()

        size = self.pygame_display_size
        flags = self.pygame_display_flags

        # [Warning]
        # PyGame seems to be running through X11 on top of wayland,
        # instead of wayland directly `pygame.display.set_mode(size, flags)`
        pygame.display.set_mode(size, flags)

        imgui.create_context()
        io = imgui.get_io()
        io.display_size = size
        io.ini_file_name = None
        io.log_file_name = None
        imgui.load_ini_settings_from_disk(str(self._imgui_ini))

        self._renderer = PygameRenderer()

        family = self._config.font.family
        family = family if family else get_default_font_path()

        if os.path.isfile(family):
            pixels = self._config.font.pixels
            scale = self._config.font.scale
            ranges = io.fonts.get_glyph_ranges_korean()
            io.fonts.clear()
            io.fonts.add_font_from_file_ttf(family, pixels * scale, None, ranges)
            io.font_global_scale /= self._config.font.scale
            self._renderer.refresh_font_texture()

        GL.glClearColor(1, 1, 1, 1)
        for win in self._windows.values():
            win.do_create()

    def on_exit(self) -> None:
        for win in self._windows.values():
            win.do_destroy()

        self._config.display.fullscreen = pygame.display.is_fullscreen()
        self._config.display.size = pygame.display.get_window_size()
        self._config.write(self._player_ini)

        if not self._imgui_ini.exists():
            self._imgui_ini.parent.mkdir(parents=True, exist_ok=True)

        imgui.save_ini_settings_to_disk(str(self._imgui_ini))

        del self._renderer
        pygame.quit()

    def on_process(self) -> None:
        while not self._done:
            self.on_event()
            self.on_frame()

    def on_event(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            self._renderer.do_event(event)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] and keys[pygame.K_q]:
            self.quit()
        if keys[pygame.K_LCTRL] and keys[pygame.K_o]:
            self.open_file()
        if keys[pygame.K_LCTRL] and keys[pygame.K_n]:
            self.open_url()
        if keys[pygame.K_LCTRL] and keys[pygame.K_LALT] and keys[pygame.K_s]:
            self._preference.opened = not self._preference.opened

        self._renderer.do_tick()

    def on_frame(self) -> None:
        imgui.new_frame()
        try:
            GL.glClear(GL.GL_COLOR_BUFFER_BIT)
            self.on_main_menu()
            self.on_popups()
            for win in self._windows.values():
                win.do_process()
            self._preference.process()
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
                    self.open_file()
                if imgui.menu_item("Open network", "Ctrl+N")[0]:
                    self.open_url()

                imgui.separator()
                _preference_opened = self._preference.opened
                if imgui.menu_item("Preference", "Ctrl+Alt+S", _preference_opened)[0]:
                    self._preference.opened = not self._preference.opened

                imgui.separator()
                if imgui.menu_item("Quit", "Ctrl+Q")[0]:
                    self.quit()
                imgui.end_menu()

            if imgui.begin_menu("Windows"):
                for key, win in self._windows.items():
                    if imgui.menu_item(key, None, win.opened)[0]:
                        win.opened = not win.opened
                if self._debug:
                    imgui.separator()
                    if imgui.menu_item("Demo", None, self._config.demo.opened)[0]:
                        self._config.demo.opened = not self._config.demo.opened
                imgui.end_menu()

    def on_popups(self) -> None:
        self._open_file_popup.process()
        self._open_url_popup.process()

    def on_demo_window(self) -> None:
        if not self._debug:
            return
        if not self._config.demo.opened:
            return
        imgui.show_test_window()
