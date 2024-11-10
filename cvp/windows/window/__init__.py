# -*- coding: utf-8 -*-

from typing import Mapping

from cvp.config.sections.window import WindowManagerConfig
from cvp.context.context import Context
from cvp.types.override import override
from cvp.widgets.manager_tab import ManagerTab
from cvp.widgets.window import Window
from cvp.widgets.window_mapper import WindowMapper
from cvp.windows.window.info import WindowInfoTab


class WindowManager(ManagerTab[WindowManagerConfig, Window]):
    def __init__(self, context: Context, windows: WindowMapper):
        super().__init__(
            context=context,
            window_config=context.config.window_manager,
            title="Window Manager",
            closable=True,
            flags=None,
        )
        self._windows = windows
        self.register(WindowInfoTab(context))

    @override
    def get_menus(self) -> Mapping[str, Window]:
        return self._windows
