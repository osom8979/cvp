# -*- coding: utf-8 -*-

import imgui

from cvp.config.config import Config


class PreferenceWindow:
    def __init__(self, config: Config):
        self._config = config
        self._flags = 0
        self._clear_color = 0.5, 0.5, 0.5, 1.0
        self._min_width = 400
        self._min_height = 300

    @property
    def opened(self) -> bool:
        return self._config.preference.opened

    @opened.setter
    def opened(self, value: bool) -> None:
        self._config.preference.opened = value

    def process(self) -> None:
        self._process_window()

    def _process_window(self) -> None:
        if not self.opened:
            return

        expanded, opened = imgui.begin("Preference", True, self._flags)
        try:
            if not opened:
                self.opened = False
                return

            if not expanded:
                return

            self._main()
        finally:
            imgui.end()

    def _main(self) -> None:
        if imgui.is_window_appearing():
            imgui.set_window_size(self._min_width, self._min_height)
