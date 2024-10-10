# -*- coding: utf-8 -*-

from typing import Mapping

import imgui

from cvp.config.sections.layout import LayoutConfig, LayoutManagerConfig
from cvp.context.context import Context
from cvp.imgui.button_ex import button_ex
from cvp.popups.confirm import ConfirmPopup
from cvp.types import override
from cvp.widgets.manager_tab import ManagerTab
from cvp.widgets.window_mapper import WindowMapper
from cvp.windows.layout.info import LayoutInfoTab


class LayoutManager(ManagerTab[LayoutManagerConfig, LayoutConfig]):
    def __init__(self, context: Context, windows: WindowMapper):
        super().__init__(
            context=context,
            window_config=context.config.layout_manager,
            title="Layout Manager",
            closable=True,
            flags=None,
        )
        self._windows = windows
        self.register(LayoutInfoTab(context, self._windows))

        self._confirm_remove = ConfirmPopup(
            title="Remove",
            label="Are you sure you want to remove layout?",
            ok="Remove",
            cancel="No",
            target=self.on_confirm_remove,
        )
        self.register_popup(self._confirm_remove)

    @override
    def get_menus(self) -> Mapping[str, LayoutConfig]:
        return {layout.uuid: layout for layout in self.context.config.layouts}

    @override
    def on_process_sidebar_top(self) -> None:
        if imgui.button("Add"):
            config = LayoutConfig(name="New Layout")
            self.context.config.layouts.append(config)
        imgui.same_line()
        selected_menu = self.latest_menus.get(self.selected)
        if button_ex("Remove", disabled=selected_menu is None):
            self._confirm_remove.show()

    def on_confirm_remove(self, value: bool) -> None:
        if not value:
            return

        selected_menu = self.latest_menus.get(self.selected)
        assert selected_menu is not None

        uuid = selected_menu.uuid
        self.context.config.remove_layout(uuid)
