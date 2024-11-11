# -*- coding: utf-8 -*-

from typing import Mapping

import imgui

from cvp.config.sections.font import FontConfig, FontManagerConfig
from cvp.context.context import Context
from cvp.types.override import override
from cvp.widgets.manager import Manager


class FontManager(Manager[FontManagerConfig, FontConfig]):
    def __init__(self, context: Context):
        super().__init__(
            context=context,
            window_config=context.config.font_manager,
            title="Font",
            closable=True,
            flags=None,
        )

    @override
    def get_menus(self) -> Mapping[str, FontConfig]:
        return {}

    @override
    def on_process_sidebar_top(self) -> None:
        pass

    @override
    def on_menu(self, key: str, item: FontConfig) -> None:
        imgui.text("Font Config")
        imgui.separator()
