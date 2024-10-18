# -*- coding: utf-8 -*-

from typing import Final

import imgui

from cvp.config.sections.onvif import HttpAuth, OnvifConfig
from cvp.context.context import Context
from cvp.imgui.button_ex import button_ex
from cvp.imgui.input_text_value import input_text_value
from cvp.logging.logging import logger
from cvp.types import override
from cvp.widgets.tab import TabItem

ENTER_RETURN: Final[int] = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE
INPUT_PASSWORD: Final[int] = imgui.INPUT_TEXT_PASSWORD
INPUT_BUFFER_SIZE: Final[int] = 2048


class OnvifAuthTab(TabItem[OnvifConfig]):
    def __init__(self, context: Context):
        super().__init__(context, "Auth")
        self._show_password = False
        self._create_runner = self.context.pm.create_thread_runner(
            self.on_create_service,
        )

    def on_create_service(self, item: OnvifConfig):
        service = self.context.create_onvif_service(item, append=True)
        services = service.update_services()
        for service in services.values():
            ns = service.Namespace
            addr = service.XAddr
            major = service.Version.Major
            minor = service.Version.Minor
            logger.info(f"{ns} ({major}.{minor}) address: {addr}")
        wsdls = service.update_wsdls()
        for wsdl in wsdls:
            logger.info(f"Update WSDL {type(wsdl).__name__}")
        return service

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
        has_service = item.uuid in self.context.om
        create_running = self._create_runner.running
        disabled_create = has_service or create_running
        disabled_clear = not has_service or create_running

        if button_ex("Create ONVIF", disabled=disabled_create):
            assert not has_service
            assert not create_running
            self._create_runner(item)

        imgui.same_line()
        if button_ex("Clear ONVIF", disabled=disabled_clear):
            assert has_service
            assert not create_running
            self.context.om.pop(item.uuid)

        onvif = self.context.om.get(item.uuid)
        if onvif is not None:
            with imgui.begin_group():
                imgui.text("ONVIF WSDL services:")
                for service in onvif.services.values():
                    ns = service.Namespace
                    addr = service.XAddr
                    major = service.Version.Major
                    minor = service.Version.Minor
                    imgui.bullet_text(f"{ns} ({major}.{minor}) address: {addr}")

            with imgui.begin_group():
                imgui.text("ONVIF WSDL services:")
                for wsdl in onvif.wsdls:
                    imgui.bullet_text(f"{type(wsdl).__name__} {wsdl.address}")
