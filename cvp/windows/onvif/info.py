# -*- coding: utf-8 -*-

from typing import Final

import imgui

from cvp.config.sections.onvif import HttpAuth, OnvifConfig
from cvp.context.context import Context
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.input_text_value import input_text_value
from cvp.types import override
from cvp.widgets.tab import TabItem

ENTER_RETURN: Final[int] = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE
INPUT_PASSWORD: Final[int] = imgui.INPUT_TEXT_PASSWORD
INPUT_BUFFER_SIZE: Final[int] = 2048


class OnvifInfoTab(TabItem[OnvifConfig]):
    def __init__(self, context: Context):
        super().__init__(context, "Info")
        self._show_password = False

    @property
    def keyrings(self):
        return self.context.home.keyrings

    @override
    def on_item(self, item: OnvifConfig) -> None:
        input_text_disabled("UUID", item.uuid)

        item.name = input_text_value(
            "Name",
            item.name,
            INPUT_BUFFER_SIZE,
        )
        item.address = input_text_value(
            "Address",
            item.address,
            INPUT_BUFFER_SIZE,
        )

        use_auth_result = imgui.checkbox("Username Token", item.use_auth)
        use_auth_changed = use_auth_result[0]
        use_auth_value = use_auth_result[1]
        assert isinstance(use_auth_changed, bool)
        assert isinstance(use_auth_value, bool)
        if use_auth_changed:
            item.use_auth = use_auth_value

        if item.use_auth:
            item.username = input_text_value(
                "Username",
                item.username,
                INPUT_BUFFER_SIZE,
            )

            password_flags = ENTER_RETURN if self._show_password else INPUT_PASSWORD
            prev_password = self.keyrings.get_onvif_password(item.uuid, str())
            next_password = input_text_value(
                "Password",
                prev_password,
                INPUT_BUFFER_SIZE,
                password_flags,
            )
            if prev_password != next_password:
                self.keyrings.set_onvif_password(item.uuid, next_password)
        else:
            self.keyrings.delete_onvif_password(item.uuid)
            input_text_disabled("Username## Disabled Username", item.username)
            input_text_disabled("Password## Disabled Password", "****")

        show_password_result = imgui.checkbox("Show Password", self._show_password)
        show_password_changed = show_password_result[0]
        show_password_value = show_password_result[1]
        assert isinstance(show_password_changed, bool)
        assert isinstance(show_password_value, bool)
        if show_password_changed:
            self._show_password = show_password_value

        encode_digest_result = imgui.checkbox("Encode digest", item.encode_digest)
        encode_digest_changed = encode_digest_result[0]
        encode_digest_value = encode_digest_result[1]
        assert isinstance(encode_digest_changed, bool)
        assert isinstance(encode_digest_value, bool)
        if encode_digest_changed:
            item.encode_digest = encode_digest_value

        imgui.text("HTTP Authorization header")
        if imgui.radio_button("None", item.http_auth is None):
            item.http_auth = None
        imgui.same_line()
        if imgui.radio_button("Basic", item.http_auth == HttpAuth.basic):
            item.http_auth = HttpAuth.basic
        imgui.same_line()
        if imgui.radio_button("Digest", item.http_auth == HttpAuth.digest):
            item.http_auth = HttpAuth.digest

        no_verify_result = imgui.checkbox("No SSL Verify", item.no_verify)
        no_verify_changed = no_verify_result[0]
        no_verify_value = no_verify_result[1]
        assert isinstance(no_verify_changed, bool)
        assert isinstance(no_verify_value, bool)
        if no_verify_changed:
            item.no_verify = no_verify_value

        if imgui.button("Test connect"):
            pass
