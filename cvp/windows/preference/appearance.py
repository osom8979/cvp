# -*- coding: utf-8 -*-

import imgui
from cvp.context.context import Context
from cvp.imgui.styles import Styles, style_colors
from cvp.logging.logging import logger
from cvp.types import override
from cvp.windows.preference._base import PreferenceWidget


class AppearancePreference(PreferenceWidget):
    def __init__(self, context: Context, label="Appearance"):
        self._section = context.config.appearance
        self._label = label
        self._styles = [str(s.name) for s in Styles]

    @property
    @override
    def label(self) -> str:
        return self._label

    @property
    def theme(self) -> str:
        return self._section.theme

    @theme.setter
    def theme(self, value: str):
        self._section.theme = value

    @property
    def theme_index(self) -> int:
        try:
            return self._styles.index(self._section.theme)
        except ValueError:
            return -1

    @override
    def on_process(self) -> None:
        imgui.text("Theme:")
        theme_result = imgui.combo("##Theme", self.theme_index, self._styles)

        theme_changed = theme_result[0]
        theme_index = theme_result[1]
        assert isinstance(theme_index, int)

        if theme_changed and 0 <= theme_index < len(self._styles):
            theme_value = self._styles[theme_index]
            try:
                style_colors(Styles(theme_value))
            except BaseException as e:
                logger.error(f"Changed theme error: {e}")
            else:
                logger.info(f"Changed theme: '{theme_value}'")
                self.theme = theme_value
