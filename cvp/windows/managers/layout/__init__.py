# -*- coding: utf-8 -*-

from typing import Mapping

from cvp.config.sections.windows.layout import LayoutSection
from cvp.config.sections.windows.manager.layout import LayoutManagerSection
from cvp.context import Context
from cvp.types import override
from cvp.widgets.hoc.manager_tab import ManagerTab
from cvp.widgets.hoc.window_mapper import WindowMapper
from cvp.windows.managers.layout.info import LayoutInfoTab


class LayoutManagerWindow(ManagerTab[LayoutManagerSection, LayoutSection]):
    def __init__(self, context: Context, windows: WindowMapper):
        super().__init__(
            context=context,
            section=context.config.layout_manager,
            title="Layout Manager",
            closable=True,
            flags=None,
        )
        self._windows = windows
        self.register(LayoutInfoTab(context, self._windows))

    @override
    def get_menus(self) -> Mapping[str, LayoutSection]:
        return self._context.config.layout_sections
