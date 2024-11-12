# -*- coding: utf-8 -*-

from typing import Mapping

import imgui

from cvp.config.sections.font import FontManagerConfig
from cvp.context.context import Context
from cvp.imgui.font_manager import FontItem, FontMapper
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.types.override import override
from cvp.widgets.manager import Manager


class FontManager(Manager[FontManagerConfig, FontItem]):
    def __init__(self, context: Context, fonts: FontMapper):
        super().__init__(
            context=context,
            window_config=context.config.font_manager,
            title="Font",
            closable=True,
            flags=None,
        )
        self._fonts = fonts

    @override
    def get_menus(self) -> Mapping[str, FontItem]:
        return {key: value for key, value in self._fonts.items()}

    @override
    def on_process_sidebar_top(self) -> None:
        pass

    @override
    def on_menu(self, key: str, item: FontItem) -> None:
        imgui.text("Font information")
        imgui.separator()

        input_text_disabled("Font family", item.family)
        input_text_disabled("Font pixel size", str(item.size_pixels))
