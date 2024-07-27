# -*- coding: utf-8 -*-

import os
from argparse import Namespace
from pathlib import Path
from typing import List, Tuple

import imgui
import pygame
from OpenGL import GL
from OpenGL.error import Error

from cvp.apps.player.config.root import RootConfig
from cvp.apps.player.interface import WindowInterface
from cvp.apps.player.renderer import PygameRenderer
from cvp.apps.player.windows.background import BackgroundWindow
from cvp.apps.player.windows.overlay import OverlayWindow


class PlayerContext:
    _renderer: PygameRenderer
    _windows: List[WindowInterface]

    def __init__(self, args: Namespace):
        self._imgui_ini = args.imgui_ini
        self._player_ini = args.player_ini
        self._debug = args.debug
        self._verbose = args.verbose

        self._config = RootConfig(self._player_ini)
        self._done = False
        self._windows = [
            BackgroundWindow(self._config),
            OverlayWindow(self._config),
        ]

    def quit(self):
        self._done = True

    def start(self) -> None:
        self.on_init()
        try:
            self.on_process()
        except Error as e:
            if str(e) == "Attempt to retrieve context when no valid context":
                raise RuntimeError("Consider enabling EGL related options") from e
        finally:
            self.on_exit()

    @property
    def pygame_display_size(self) -> Tuple[int, int]:
        assert pygame.display.get_init(), "pygame must be initialized"

        w = self._config.display_width
        h = self._config.display_height
        if w >= 1 and h >= 1:
            return w, h
        else:
            info = pygame.display.Info()
            return info.current_w, info.current_h

    @property
    def pygame_display_flags(self) -> int:
        common_flags = pygame.DOUBLEBUF | pygame.OPENGL
        if self._config.display_fullscreen:
            return common_flags | pygame.FULLSCREEN
        else:
            return common_flags | pygame.RESIZABLE

    def on_init(self) -> None:
        if self._config.display_force_egl:
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
        imgui.load_ini_settings_from_disk(self._imgui_ini)

        if os.path.isfile(self._config.font_family):
            io.fonts.clear()
            io.fonts.add_font_from_file_ttf(
                self._config.font_family,
                self._config.font_pixels * self._config.font_scale,
                None,
                io.fonts.get_glyph_ranges_korean(),
            )
            io.font_global_scale /= self._config.font_scale
            self._renderer.refresh_font_texture()

        GL.glClearColor(1, 1, 1, 1)
        for win in self._windows:
            win.on_create()

    def on_exit(self) -> None:
        for win in self._windows:
            win.on_destroy()

        self._config.display_fullscreen = pygame.display.is_fullscreen()
        self._config.display_size = pygame.display.get_window_size()
        self._config.write(self._player_ini)

        Path(self._imgui_ini).parent.mkdir(parents=True, exist_ok=True)
        imgui.save_ini_settings_to_disk(self._imgui_ini)

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
                if imgui.menu_item("Overlay", None, self._config.views_overlay)[0]:
                    self._config.views_overlay = not self._config.views_overlay
                imgui.end_menu()

            if imgui.begin_menu("Tools"):
                if self._debug:
                    imgui.separator()
                    if imgui.menu_item("Demo", None, self._config.tools_demo)[0]:
                        self._config.tools_demo = not self._config.tools_demo

                imgui.end_menu()

    def on_demo_window(self) -> None:
        if not self._debug:
            return
        if not self._config.tools_demo:
            return
        imgui.show_test_window()
