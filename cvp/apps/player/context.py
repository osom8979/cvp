# -*- coding: utf-8 -*-

import os
from argparse import Namespace
from typing import Dict, Optional, Tuple, Union

import imgui
import pygame
from OpenGL import GL
from OpenGL.error import Error

from cvp.config.config import Config
from cvp.config.sections.display import force_egl_section_key
from cvp.filesystem.permission import test_directory, test_readable
from cvp.logging.logging import (
    convert_level_number,
    dumps_default_logging_config,
    loads_logging_config,
    logger,
    set_root_level,
)
from cvp.popups.input_text import InputTextPopup
from cvp.popups.open_file import OpenFilePopup
from cvp.process.manager import ProcessManager
from cvp.renderer.renderer import PygameRenderer
from cvp.resources.home import HomeDir
from cvp.widgets.fonts import add_jbm_font, add_ngc_font

# noinspection PyProtectedMember
from cvp.widgets.hoc.window import Window
from cvp.widgets.styles import default_style_colors
from cvp.windows.media import MediaWindow
from cvp.windows.medias import MediasWindow
from cvp.windows.mpv import MpvWindow
from cvp.windows.overlay import OverlayWindow
from cvp.windows.preference import PreferenceWindow
from cvp.windows.processes import ProcessesWindow


class PlayerContext:
    _renderer: PygameRenderer
    _windows: Dict[str, Window]

    def __init__(
        self,
        home: Optional[Union[str, os.PathLike[str]]] = None,
        debug=False,
        verbose=0,
    ):
        self._home = HomeDir.from_path(home)
        self._debug = debug
        self._verbose = verbose
        self._done = False

        if not self._home.exists():
            self._home.mkdir(parents=True, exist_ok=True)

        test_directory(self._home)
        test_readable(self._home)

        self._readonly = not os.access(self._home, os.W_OK)
        self._config = Config(self._home.cvp_ini, self._home)

        logging_config_path = self._config.logging.config_path
        if os.path.isfile(logging_config_path):
            loads_logging_config(logging_config_path)
            logger.info(f"Loads the logging config file: '{logging_config_path}'")

        root_severity = self._config.logging.root_severity
        if root_severity:
            level = convert_level_number(root_severity)
            set_root_level(level)
            logger.log(level, f"Changed root severity: {root_severity}")

        if self._config.developer.has_debug:
            self._debug = self._config.developer.debug
            logger.info(f"Changed debug mode: {self._debug}")

        if self._config.developer.has_verbose:
            self._verbose = self._config.developer.verbose
            logger.info(f"Changed verbose level: {self._verbose}")

        thread_workers = self._config.concurrency.thread_workers
        process_workers = self._config.concurrency.process_workers
        self._pm = ProcessManager(
            self._config.ffmpeg,
            home=self._home,
            thread_workers=thread_workers,
            process_workers=process_workers,
        )

        self._windows = {
            "__overlay__": OverlayWindow(self._config.overlay),
            "__mpv__": MpvWindow(self._config.mpv),
        }
        self._medias = MediasWindow(self._pm, self._config)
        self._processes = ProcessesWindow(self._pm, self._config)
        self._preference = PreferenceWindow(self._config)
        for config in self._config.medias.values():
            self._windows[config.section] = MediaWindow(config, self._pm)

        self._open_file_popup = OpenFilePopup(title="Open file")
        self._open_url_popup = InputTextPopup(
            title="Open network stream",
            label="Please enter a network URL:",
            ok="Open",
            cancel="Close",
        )

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

    def add_media_window(self, file: str) -> None:
        section = self._config.add_media_section()
        section.opened = True
        section.file = file
        section.name = file

        window = MediaWindow(section, self._pm)
        window.do_create()

        self._windows[section.section] = window

    def start(self) -> None:
        self.on_init()
        try:
            self.on_process()
        except Error as e:
            if str(e) == "Attempt to retrieve context when no valid context":
                section, key = force_egl_section_key()
                logger.error(
                    f"Please modify the value of '{key}' to 'True' in the '[{section}]'"
                    f" section of the '{str(self._home.cvp_ini)}' file and try again."
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
        imgui.load_ini_settings_from_disk(str(self._home.imgui_ini))

        self._renderer = PygameRenderer()

        io.fonts.clear()
        pixels = self._config.font.pixels
        scale = self._config.font.scale
        font_size_pixels = pixels * scale
        add_jbm_font(font_size_pixels)
        add_ngc_font(font_size_pixels)

        user_font = self._config.font.family
        if user_font and os.path.isfile(user_font):
            korean_ranges = io.fonts.get_glyph_ranges_korean()
            io.fonts.add_font_from_file_ttf(user_font, font_size_pixels, korean_ranges)

        io.font_global_scale /= self._config.font.scale
        self._renderer.refresh_font_texture()

        theme = self._config.appearance.theme
        default_style_colors(theme)

        GL.glClearColor(0, 0, 0, 1)
        for win in self._windows.values():
            win.do_create()

    def on_exit(self) -> None:
        self._pm.teardown(self._config.processes.teardown_timeout)

        for win in self._windows.values():
            win.do_destroy()

        if not self._readonly:
            if not self._home.is_dir():
                self._home.mkdir(parents=True, exist_ok=True)

            self._config.display.fullscreen = pygame.display.is_fullscreen()
            self._config.display.size = pygame.display.get_window_size()
            self._config.write(self._home.cvp_ini)

            if not self._home.logging_json.exists():
                logging_json = dumps_default_logging_config(self._home)
                self._home.logging_json.write_text(logging_json)

            if not self._home.imgui_ini.exists():
                self._home.imgui_ini.parent.mkdir(parents=True, exist_ok=True)
                imgui.save_ini_settings_to_disk(str(self._home.imgui_ini))

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
            self._medias.do_process()
            self._processes.do_process()
            self._preference.do_process()
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
        file = self._open_file_popup.do_process()
        if file:
            self.add_media_window(file)

        url = self._open_url_popup.do_process()
        if url:
            self.add_media_window(url)

    def on_demo_window(self) -> None:
        if not self._debug:
            return
        if not self._config.demo.opened:
            return
        imgui.show_test_window()
