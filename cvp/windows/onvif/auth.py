# -*- coding: utf-8 -*-

from typing import Final, Optional

import imgui

from cvp.config.sections.onvif import HttpAuth, OnvifConfig
from cvp.context.context import Context
from cvp.imgui.button_ex import button_ex
from cvp.imgui.input_text_value import input_text_value
from cvp.logging.logging import onvif_logger as logger
from cvp.onvif.ver10.devicemgmt import OnvifDeviceManagement
from cvp.types import override
from cvp.widgets.tab import TabItem

ENTER_RETURN: Final[int] = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE
INPUT_PASSWORD: Final[int] = imgui.INPUT_TEXT_PASSWORD
INPUT_BUFFER_SIZE: Final[int] = 2048


class OnvifAuthTab(TabItem[OnvifConfig]):
    def __init__(self, context: Context):
        super().__init__(context, "Auth")
        self._show_password = False
        self._requesting = False

    def get_services(self, onvif_config: OnvifConfig) -> None:
        if self._requesting:
            raise ValueError("Now requesting")

        self._requesting = True
        password = self.keyrings.get_onvif_password(onvif_config.uuid, str())
        self.context.pm.submit_thread(self._get_services_main, onvif_config, password)

    def _get_services_main(
        self,
        onvif_config: OnvifConfig,
        password: Optional[str] = None,
    ) -> None:
        try:
            api = OnvifDeviceManagement(
                onvif_config=onvif_config,
                wsdl_config=self.context.config.wsdl,
                home=self.context.home,
                password=password,
            )
            result = api.get_services()
            logger.info(result)
        finally:
            self._requesting = False

    @property
    def keyrings(self):
        return self.context.home.keyrings

    def on_wsse_process(self, item: OnvifConfig) -> None:
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

        show_password = imgui.checkbox("Show Password", self._show_password)
        show_password_changed = show_password[0]
        show_password_value = show_password[1]
        assert isinstance(show_password_changed, bool)
        assert isinstance(show_password_value, bool)
        if show_password_changed:
            self._show_password = show_password_value

        imgui.text("Password Type:")
        if imgui.radio_button("PasswordText", item.http_auth is None):
            item.encode_digest = False
        if imgui.is_item_hovered():
            with imgui.begin_tooltip():
                imgui.text('Use <wsse:Password Type="wsse:PasswordText">')
        imgui.same_line()
        if imgui.radio_button("PasswordDigest", item.http_auth == HttpAuth.basic):
            item.encode_digest = True
        if imgui.is_item_hovered():
            with imgui.begin_tooltip():
                imgui.text('Use <wsse:Password Type="wsse:PasswordDigest">')

        imgui.text("HTTP Authorization header:")
        if imgui.radio_button("None", item.http_auth is None):
            item.http_auth = None
        imgui.same_line()
        if imgui.radio_button("Basic", item.http_auth == HttpAuth.basic):
            item.http_auth = HttpAuth.basic
        imgui.same_line()
        if imgui.radio_button("Digest", item.http_auth == HttpAuth.digest):
            item.http_auth = HttpAuth.digest

    @override
    def on_item(self, item: OnvifConfig) -> None:
        use_wsse = imgui.checkbox("Use WS-Security", item.use_wsse)
        if imgui.is_item_hovered():
            with imgui.begin_tooltip():
                imgui.text("Use <wsse:UsernameToken> in <soap:Header>")
        use_wsse_changed = use_wsse[0]
        use_wsse_value = use_wsse[1]
        assert isinstance(use_wsse_changed, bool)
        assert isinstance(use_wsse_value, bool)
        if use_wsse_changed:
            item.use_wsse = use_wsse_value

        if item.use_wsse:
            self.on_wsse_process(item)

        imgui.separator()
        if button_ex("Get services", disabled=self._requesting):
            self.get_services(item)

        if imgui.is_item_hovered():
            with imgui.begin_tooltip():
                imgui.text("Returns information about services on the device")
