# -*- coding: utf-8 -*-

from pprint import pformat
from types import MappingProxyType
from typing import Callable, Dict, Final, Sequence, Tuple, TypeAlias

import imgui

from cvp.config.sections.onvif import OnvifConfig
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child
from cvp.imgui.button_ex import button_ex
from cvp.imgui.item_width import item_width
from cvp.imgui.slider_float import slider_float
from cvp.inspect.argument import Argument
from cvp.onvif.client import OnvifClient
from cvp.types import override
from cvp.widgets.tab import TabItem
from cvp.wsdl.client import WsdlClient
from cvp.wsdl.operation import WsdlOperationProxy

NOT_FOUND_INDEX: Final[int] = -1


class StepDone(RuntimeError):
    pass


def _bool_handler(argument: Argument) -> None:
    changed, value = imgui.checkbox(argument.name, argument.get_value(False))
    assert isinstance(changed, bool)
    assert isinstance(value, bool)
    if changed:
        argument.value = value

    if argument.doc and imgui.is_item_hovered():
        with imgui.begin_tooltip():
            imgui.text(argument.doc)


def _int_handler(argument: Argument) -> None:
    changed, value = imgui.input_int(argument.name, argument.get_value(0))
    assert isinstance(changed, bool)
    assert isinstance(value, int)
    if changed:
        argument.value = value

    if argument.doc and imgui.is_item_hovered():
        with imgui.begin_tooltip():
            imgui.text(argument.doc)


ArgumentRendererMapper: TypeAlias = MappingProxyType[type, Callable[[Argument], None]]

DEFAULT_ARGUMENT_RENDERERS = ArgumentRendererMapper(
    {
        bool: _bool_handler,
        int: _int_handler,
    }
)


class OnvifApisTab(TabItem[OnvifConfig]):
    def __init__(self, context: Context):
        super().__init__(context, "APIs")
        self._request_runner = self.context.pm.create_thread_runner(self.on_api_request)
        self._error_color = 1.0, 0.0, 0.0, 1.0
        self._warning_color = 1.0, 1.0, 0.0, 1.0
        self._typename_color = 1.0, 0.647, 0.0, 1.0
        self._left_width = 180.0
        self._min_left_width = 100.0
        self._max_left_width = 300.0

    @staticmethod
    def on_api_request(operation: WsdlOperationProxy):
        operation.call_with_arguments()

    @override
    def on_item(self, item: OnvifConfig) -> None:
        try:
            onvif = self.process_onvif_client(item)
            binding_index, binding_name = self.process_binding_index(item, onvif.wsdls)
            apis = self.process_apis(onvif.wsdls, binding_index)
            api_name = self.process_select_api(item, apis)
            imgui.same_line()
            self.process_api_details(onvif, binding_name, apis, api_name)
        except StepDone:
            pass

    def process_onvif_client(self, item: OnvifConfig) -> OnvifClient:
        onvif = self.context.om.get(item.uuid)

        if onvif is None:
            warning_message_line0 = "ONVIF service instance does not exist."
            imgui.text_colored(warning_message_line0, *self._warning_color)

            warning_message_line1 = "Please create a service instance first."
            imgui.text_colored(warning_message_line1, *self._warning_color)

            raise StepDone("ONVIF service instance does not exist")

        return onvif

    def process_binding_index(
        self,
        item: OnvifConfig,
        wsdls: Sequence[WsdlClient],
    ) -> Tuple[int, str]:
        bindings = [wsdl.binding_name for wsdl in wsdls]

        if not bindings:
            warning_message = "There are no bindings to choose from."
            imgui.text_colored(warning_message, *self._warning_color)

            raise StepDone("ONVIF binding does not exist")

        try:
            binding_index = bindings.index(item.select_binding)
        except ValueError:
            binding_index = NOT_FOUND_INDEX

        with item_width(-1):
            binding_result = imgui.combo(
                "## Binding",
                binding_index,
                bindings,
            )

        binding_changed = binding_result[0]
        binding_index = binding_result[1]
        assert isinstance(binding_changed, bool)
        assert isinstance(binding_index, int)

        if binding_changed and 0 <= binding_index < len(bindings):
            item.select_binding = bindings[binding_index]

        if not item.select_binding:
            warning_message = "You must select a binding service."
            imgui.text_colored(warning_message, *self._warning_color)

            raise StepDone("ONVIF binding is not selected")

        return binding_index, item.select_binding

    def process_apis(
        self,
        wsdls: Sequence[WsdlClient],
        binding_index: int,
    ) -> Dict[str, WsdlOperationProxy]:
        apis = wsdls[binding_index].service_operations

        if not apis:
            warning_message = "There are no APIs to choose from."
            imgui.text_colored(warning_message, *self._warning_color)

            raise StepDone("ONVIF API does not exist")

        return apis

    def process_select_api(
        self,
        item: OnvifConfig,
        apis: Dict[str, WsdlOperationProxy],
    ) -> str:
        with begin_child("API List", width=self._left_width):
            with item_width(-1):
                left_width = slider_float(
                    "## API List Width",
                    self._left_width,
                    self._min_left_width,
                    self._max_left_width,
                    "List width (%.3f)",
                )
                if left_width:
                    self._left_width = left_width.value

                list_box = imgui.begin_list_box("## API List Box", width=-1, height=-1)
                if list_box.opened:
                    with list_box:
                        for key in apis.keys():
                            if imgui.selectable(key, key == item.select_api)[1]:
                                item.select_api = key

        return item.select_api

    def process_api_details(
        self,
        onvif: OnvifClient,
        binding_name: str,
        apis: Dict[str, WsdlOperationProxy],
        api_name: str,
    ) -> None:
        with begin_child("API Details", border=True):
            if api_name not in apis:
                warning_message = "You must select an API."
                imgui.text_colored(warning_message, *self._warning_color)

                raise StepDone("ONVIF API is not selected")

            imgui.text(api_name)
            imgui.separator()

            imgui.text("Parameters:")
            operation = apis[api_name]

            mishandling = self.process_operation(operation)

            disable_request = (
                mishandling >= 1
                or not operation.arguments.requestable
                or bool(self._request_runner)
            )

            if button_ex("Request", disabled=disable_request):
                self._request_runner(operation)

            imgui.same_line()

            has_latest = operation.has_latest()
            has_cache = operation.has_cache()
            disable_remove_cache = not has_latest and not has_cache

            if button_ex("Remove Cache", disabled=disable_remove_cache):
                if has_latest:
                    operation.clear_latest()
                    has_latest = False
                if has_cache:
                    operation.remove_cache()
                    has_cache = False

            if has_latest or has_cache:
                imgui.text("Response:")
                with begin_child("Response", border=True):
                    if has_latest:
                        response = operation.latest
                    elif has_cache:
                        response = operation.read_cache()
                        if not has_latest:
                            operation.latest = response
                    else:
                        assert False, "Inaccessible section"

                    imgui.text_unformatted(pformat(response))

    def process_operation(self, operation: WsdlOperationProxy) -> int:
        mishandling = 0
        for name, argument in operation.arguments.items():
            try:
                self.process_argument(argument)
            except StepDone:
                mishandling += 1
        return mishandling

    def process_argument(self, argument: Argument) -> None:
        assert not argument.is_empty_annotation
        assert argument.is_annotated

        arg_type = argument.type_deduction
        typename = arg_type.__name__ if isinstance(arg_type, type) else str(arg_type)
        assert isinstance(typename, str)

        # default = argument.default
        # annotation = argument.annotation
        # kind = argument.kind
        # empty_value = argument.is_empty_value
        # value = argument.value

        handler = DEFAULT_ARGUMENT_RENDERERS.get(argument.type_deduction)
        if handler:
            handler(argument)
        else:
            imgui.text_colored(f"{argument.name} <{typename}>", *self._error_color)
            raise StepDone(f"Could not find handler for argument of type <{typename}>")
