# -*- coding: utf-8 -*-

from typing import Final

import imgui

from cvp.config.sections.toast import ToastWindowConfig
from cvp.context.context import Context
from cvp.renderer.window.base import WindowBase
from cvp.types.override import override

TOAST_WINDOW_FLAGS: Final[int] = (
    imgui.WINDOW_NO_DECORATION
    | imgui.WINDOW_ALWAYS_AUTO_RESIZE
    | imgui.WINDOW_NO_SAVED_SETTINGS
    | imgui.WINDOW_NO_NAV
    | imgui.WINDOW_NO_MOVE
)


class ToastWindow(WindowBase[ToastWindowConfig]):
    def __init__(self, context: Context):
        super().__init__(
            context=context,
            window_config=context.config.toast_window,
            title="Toast",
            closable=False,
            flags=TOAST_WINDOW_FLAGS,
        )

    @override
    def on_process(self) -> None:
        pass
