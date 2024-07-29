# -*- coding: utf-8 -*-

import os
from argparse import Namespace
from pathlib import Path
from typing import List, Optional, Tuple

import imgui
import pygame
from OpenGL import GL
from OpenGL.error import Error

from cvp.apps.player.interface import WindowInterface
from cvp.arguments import CVP_HOME, IMGUI_INI_FILENAME, PLAYER_INI_FILENAME
from cvp.config.root import Config
from cvp.config.sections.display import force_egl_pair
from cvp.filesystem.permission import test_rw_directory
from cvp.logging.logging import logger
from cvp.renderer.renderer import PygameRenderer
from cvp.windows.background import BackgroundWindow
from cvp.windows.overlay import OverlayWindow


class PlayerContext:
    _renderer: PygameRenderer
    _windows: List[WindowInterface]

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

        test_rw_directory(self._home)

        self._config = Config(self._player_ini)
        self._done = False
        self._windows = [
            BackgroundWindow(self._config),
            OverlayWindow(self._config.overlay),
        ]

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

    def start(self) -> None:
        self.on_init()
        try:
            self.on_process()
        except Error as e:
            if str(e) == "Attempt to retrieve context when no valid context":
                section, key = force_egl_pair()
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
        self._renderer = PygameRenderer()
        io = imgui.get_io()
        io.display_size = size
        imgui.load_ini_settings_from_disk(str(self._imgui_ini))

        if os.path.isfile(self._config.font.family):
            io.fonts.clear()
            io.fonts.add_font_from_file_ttf(
                self._config.font.family,
                self._config.font.pixels * self._config.font.scale,
                None,
                io.fonts.get_glyph_ranges_korean(),
            )
            io.font_global_scale /= self._config.font.scale
            self._renderer.refresh_font_texture()

        GL.glClearColor(1, 1, 1, 1)
        for win in self._windows:
            win.on_create()

    def on_exit(self) -> None:
        for win in self._windows:
            win.on_destroy()

        self._config.display.fullscreen = pygame.display.is_fullscreen()
        self._config.display.size = pygame.display.get_window_size()
        self._config.write(self._player_ini)

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

        self._renderer.do_tick()

    def on_frame(self) -> None:
        imgui.new_frame()
        try:
            GL.glClear(GL.GL_COLOR_BUFFER_BIT)
            self.on_main_menu()
            for win in self._windows:
                win.on_process()
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
                imgui.separator()
                if imgui.menu_item("Quit", "Ctrl+Q")[0]:
                    self.quit()
                imgui.end_menu()

            if imgui.begin_menu("View"):
                if imgui.menu_item("Overlay", None, self._config.overlay.visible)[0]:
                    self._config.overlay.visible = not self._config.overlay.visible
                imgui.end_menu()

            if imgui.begin_menu("Tools"):
                if self._debug:
                    imgui.separator()
                    if imgui.menu_item("Demo", None, self._config.tools.demo)[0]:
                        self._config.tools.demo = not self._config.tools.demo

                imgui.end_menu()

    def on_demo_window(self) -> None:
        if not self._debug:
            return
        if not self._config.tools.demo:
            return
        imgui.show_test_window()
