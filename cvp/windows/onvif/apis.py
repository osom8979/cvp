# -*- coding: utf-8 -*-

from pprint import pformat
from typing import Dict, Final, Tuple

import imgui
from zeep.proxy import OperationProxy

from cvp.config.sections.onvif import OnvifConfig
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child
from cvp.imgui.button_ex import button_ex
from cvp.types import override
from cvp.widgets.tab import TabItem
from cvp.widgets.wsdl_operation import WsdlOperationWidget

NOT_FOUND_INDEX: Final[int] = -1


class OnvifApisTab(TabItem[OnvifConfig]):
    _widgets: Dict[Tuple[str, str, str], WsdlOperationWidget]

    def __init__(self, context: Context):
        super().__init__(context, "APIs")
        self._request_runner = self.context.pm.create_thread_runner(self.on_api_request)
        self._warning_color = 1.0, 1.0, 0.0, 1.0
        self._select_binding = str()
        self._select_api = str()
        self._widgets = dict()

    def on_api_request(self, item: OnvifConfig, operation: OperationProxy):
        pass

    @override
    def on_item(self, item: OnvifConfig) -> None:
        onvif = self.context.om.get(item.uuid)
        if onvif is None:
            warning_message = (
                "ONVIF service instance does not exist."
                " Please create a service instance first."
            )
            imgui.text_colored(warning_message, *self._warning_color)
            return

        wsdls = onvif.wsdls
        bindings = [wsdl.binding_name for wsdl in wsdls]
        if not bindings:
            warning_message = "There are no bindings to choose from."
            imgui.text_colored(warning_message, *self._warning_color)
            return

        try:
            binding_index = bindings.index(self._select_binding)
        except ValueError:
            binding_index = NOT_FOUND_INDEX

        binding_result = imgui.combo(
            "Binding",
            binding_index,
            bindings,
        )
        binding_changed = binding_result[0]
        binding_index = binding_result[1]
        assert isinstance(binding_index, int)
        if binding_changed and 0 <= binding_index < len(bindings):
            self._select_binding = bindings[binding_index]

        if not self._select_binding:
            warning_message = "You must select a binding service."
            imgui.text_colored(warning_message, *self._warning_color)
            return

        service = wsdls[binding_index]
        apis = service.binding_operations

        if not apis:
            warning_message = "There are no APIs to choose from."
            imgui.text_colored(warning_message, *self._warning_color)
            return

        list_box = imgui.begin_list_box("## API List", width=0, height=-1)
        if list_box.opened:
            with list_box:
                for key in apis.keys():
                    if imgui.selectable(key, key == self._select_api)[1]:
                        self._select_api = key

        imgui.same_line()

        with begin_child("API Details", border=True):
            if self._select_api not in apis:
                warning_message = "You must select an API."
                imgui.text_colored(warning_message, *self._warning_color)
                return

            imgui.text(self._select_api)
            imgui.separator()

            imgui.text("Parameters:")
            operation = apis[self._select_api]

            widget_key = onvif.uuid, self._select_binding, self._select_api
            if widget_key not in self._widgets:
                widget = WsdlOperationWidget(operation)
                self._widgets[widget_key] = widget
            else:
                widget = self._widgets[widget_key]

            widget.on_process()

            has_cache = onvif.has_cache(self._select_binding, self._select_api)

            if button_ex("Request", disabled=self._request_runner):
                self._request_runner(item, operation)
            imgui.same_line()
            if button_ex("Remove Cache", disabled=not has_cache):
                onvif.remove_cache(self._select_binding, self._select_api)
                has_cache = False

            if has_cache:
                imgui.text("Response:")
                with begin_child("Response", border=True):
                    response = onvif.read_cache(self._select_binding, self._select_api)
                    imgui.text_unformatted(pformat(response))
