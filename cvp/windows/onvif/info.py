# -*- coding: utf-8 -*-

from typing import Final

import imgui

from cvp.config.sections.onvif import OnvifConfig
from cvp.context.context import Context
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.item_width import item_width
from cvp.types import override
from cvp.widgets.tab import TabItem

ENTER_RETURNS: Final[int] = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE
INPUT_BUFFER_SIZE: Final[int] = 2048


class OnvifInfoTab(TabItem[OnvifConfig]):
    def __init__(self, context: Context):
        super().__init__(context, "Info")

    @override
    def on_item(self, item: OnvifConfig) -> None:
        imgui.text("UUID:")
        input_text_disabled("## UUID", item.uuid)

        imgui.text("Name:")
        with item_width(-1):
            changed_name, value_name = imgui.input_text(
                "## Name",
                item.name,
                INPUT_BUFFER_SIZE,
                ENTER_RETURNS,
            )
            assert isinstance(changed_name, bool)
            assert isinstance(value_name, str)
            if changed_name:
                item.name = value_name

        imgui.text("Address:")
        with item_width(-1):
            changed_address, value_address = imgui.input_text(
                "## Address",
                item.address,
                INPUT_BUFFER_SIZE,
                ENTER_RETURNS,
            )
            assert isinstance(changed_address, bool)
            assert isinstance(value_address, str)
            if changed_address:
                item.address = value_address
