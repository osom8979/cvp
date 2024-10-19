# -*- coding: utf-8 -*-

from typing import Final

import imgui

from cvp.config.sections.onvif import OnvifConfig
from cvp.context.context import Context
from cvp.types import override
from cvp.widgets.tab import TabItem

ENTER_RETURN: Final[int] = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE
INPUT_PASSWORD: Final[int] = imgui.INPUT_TEXT_PASSWORD
INPUT_BUFFER_SIZE: Final[int] = 2048


class OnvifApisTab(TabItem[OnvifConfig]):
    def __init__(self, context: Context):
        super().__init__(context, "APIs")
        self._request_runner = self.context.pm.create_thread_runner(self.on_api_request)

    def on_api_request(self, item: OnvifConfig):
        pass

    @override
    def on_item(self, item: OnvifConfig) -> None:
        imgui.separator()
