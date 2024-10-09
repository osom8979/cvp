# -*- coding: utf-8 -*-

from typing import Mapping

import imgui
from cvp.config.sections.wsd import WsdConfig, WsdManagerConfig
from cvp.context.context import Context
from cvp.types import override
from cvp.widgets.manager import Manager


class WsdManager(Manager[WsdManagerConfig, WsdConfig]):
    def __init__(self, context: Context):
        super().__init__(
            context=context,
            window_config=context.config.wsd_manager,
            title="WsDiscovery",
            closable=True,
            flags=None,
        )

    @override
    def get_menus(self) -> Mapping[str, WsdConfig]:
        return {wsd.uuid: wsd for wsd in self.context.config.wsds}

    @override
    def on_process_sidebar_top(self) -> None:
        imgui.button("Discovery")

    @override
    def on_menu(self, key: str, item: WsdConfig) -> None:
        imgui.text("Web Services Dynamic Discovery")
        imgui.separator()
