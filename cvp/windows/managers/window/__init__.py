# -*- coding: utf-8 -*-

from typing import Mapping

from cvp.config.sections.windows.manager.window import WindowManagerSection
from cvp.context import Context
from cvp.types import override
from cvp.widgets.hoc.manager_tab import ManagerTab
from cvp.widgets.hoc.window import Window
from cvp.widgets.hoc.window_mapper import WindowMapper
from cvp.windows.managers.window.info import WindowInfoTab


class WindowManagerWindow(ManagerTab[WindowManagerSection, Window]):
    def __init__(self, context: Context, windows: WindowMapper):
        super().__init__(
            context=context,
            section=context.config.window_manager,
            title="Window Manager",
            closable=True,
            flags=None,
        )
        self._windows = windows
        self.register(WindowInfoTab(context))

    @override
    def get_menus(self) -> Mapping[str, Window]:
        return self._windows