# -*- coding: utf-8 -*-

from typing import Final

import imgui

from cvp.config.sections.onvif import OnvifConfig
from cvp.context.context import Context
from cvp.imgui.button_ex import button_ex
from cvp.logging.logging import logger
from cvp.types import override
from cvp.widgets.tab import TabItem

TABLE_FLAGS: Final[int] = (
    imgui.TABLE_SIZING_FIXED_FIT
    | imgui.TABLE_ROW_BACKGROUND
    | imgui.TABLE_BORDERS
    | imgui.TABLE_RESIZABLE
    | imgui.TABLE_REORDERABLE
    | imgui.TABLE_HIDEABLE
)


class OnvifServiceTab(TabItem[OnvifConfig]):
    def __init__(self, context: Context):
        super().__init__(context, "Service")
        self._error_color = 1.0, 0.0, 0.0, 1.0
        self._update_runner = self.context.pm.create_thread_runner(
            self.on_update_service,
        )

    def on_update_service(self, item: OnvifConfig):
        onvif = self.context.om.sync(item)
        for service in onvif.update_services().values():
            ns = service.Namespace
            addr = service.XAddr
            major = service.Version.Major
            minor = service.Version.Minor
            logger.info(f"{ns} ({major}.{minor}) address is '{addr}'")
        for wsdl in onvif.update_wsdls():
            logger.info(f"Update WSDL {type(wsdl).__name__}")
        return onvif

    @override
    def on_item(self, item: OnvifConfig) -> None:
        has_service = item.uuid in self.context.om
        update_running = self._update_runner.running
        has_error = bool(self._update_runner.error)
        disabled_clear = not has_service or update_running

        if button_ex("Update ONVIF Service", disabled=update_running):
            assert not update_running
            self._update_runner(item)

        imgui.same_line()
        if button_ex("Remove ONVIF Service", disabled=disabled_clear):
            assert has_service
            assert not update_running
            self.context.om.pop(item.uuid)

        if has_error:
            imgui.text_colored(
                type(self._update_runner.error).__name__,
                *self._error_color,
            )

        onvif = self.context.om.get(item.uuid)
        if onvif is not None:
            imgui.text("Services:")
            services_table = imgui.begin_table("ServicesTable", 3, TABLE_FLAGS)
            if services_table.opened:
                imgui.table_setup_column("Namespace", imgui.TABLE_COLUMN_WIDTH_STRETCH)
                imgui.table_setup_column("Version", imgui.TABLE_COLUMN_WIDTH_FIXED)
                imgui.table_setup_column("Address", imgui.TABLE_COLUMN_WIDTH_STRETCH)
                imgui.table_headers_row()

                with services_table:
                    for service in onvif.services.values():
                        imgui.table_next_row()
                        imgui.table_set_column_index(0)
                        imgui.text(service.Namespace)
                        imgui.table_set_column_index(1)
                        imgui.text(f"{service.Version.Major}.{service.Version.Minor}")
                        imgui.table_set_column_index(2)
                        imgui.text(service.XAddr)

            imgui.text("ONVIF WSDL services:")
            wsdl_table = imgui.begin_table("WsdlTable", 3, TABLE_FLAGS)
            if wsdl_table.opened:
                imgui.table_setup_column("Class", imgui.TABLE_COLUMN_WIDTH_FIXED)
                imgui.table_setup_column("Binding", imgui.TABLE_COLUMN_WIDTH_FIXED)
                imgui.table_setup_column("Address", imgui.TABLE_COLUMN_WIDTH_STRETCH)
                imgui.table_headers_row()

                with wsdl_table:
                    for wsdl in onvif.wsdls:
                        imgui.table_next_row()
                        imgui.table_set_column_index(0)
                        imgui.text(type(wsdl).__name__)
                        imgui.table_set_column_index(1)
                        imgui.text(wsdl.binding_name)
                        imgui.table_set_column_index(2)
                        imgui.text(wsdl.address)
