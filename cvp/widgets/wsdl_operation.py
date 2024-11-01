# -*- coding: utf-8 -*-

from typing import Callable, Dict, Final

import imgui

from cvp.inspect.argument import Argument
from cvp.types import override
from cvp.variables import ZEEP_ELEMENT_SEPARATOR
from cvp.widgets.widget import WidgetInterface
from cvp.wsdl.operation import WsdlOperationProxy

INPUT_BUFFER_SIZE: Final[int] = 2048


class WsdlOperationWidget(WidgetInterface):
    _handlers: Dict[type, Callable[[Argument], None]]

    def __init__(
        self,
        operation: WsdlOperationProxy,
        element_separator=ZEEP_ELEMENT_SEPARATOR,
    ):
        self._operation = operation
        self._element_separator = element_separator
        self._error_color = 1.0, 0.0, 0.0, 1.0
        self._handlers = {
            bool: self.do_boolean,
            int: self.do_integer,
        }

    @property
    def name(self) -> str:
        return self._operation.name

    def value_key(self, argument: Argument, parent_name: str) -> str:
        return f"{parent_name}{self._element_separator}{argument.name}"

    @staticmethod
    def do_tooltip(argument: Argument) -> None:
        if argument.doc and imgui.is_item_hovered():
            with imgui.begin_tooltip():
                imgui.text(argument.doc)

    def do_boolean(self, argument: Argument) -> None:
        changed, value = imgui.checkbox(argument.name, argument.get_value(False))
        self.do_tooltip(argument)
        assert isinstance(changed, bool)
        assert isinstance(value, bool)
        if changed:
            argument.value = value

    def do_integer(self, argument: Argument) -> None:
        changed, value = imgui.input_int(argument.name, argument.get_value(0))
        self.do_tooltip(argument)
        assert isinstance(changed, bool)
        assert isinstance(value, int)
        if changed:
            argument.value = value

    # def _render_complex(self, element: Element, parent: str) -> None:
    #     key = self.value_key(element, parent)
    #     if imgui.tree_node(f"{element.name}###{key}", imgui.TREE_NODE_DEFAULT_OPEN):
    #         for child_name, child_element in element.type.elements:
    #             self.render_element(child_element, key)
    #         imgui.tree_pop()
    #
    # def _render_string(self, element: Element, parent: str) -> None:
    #     key = self.value_key(element, parent)
    #     changed, value = imgui.input_text(
    #         f"{element.name}###{key}",
    #         self._input_values.get(key, str()),
    #         INPUT_BUFFER_SIZE,
    #     )
    #     assert isinstance(changed, bool)
    #     assert isinstance(value, str)
    #     if changed:
    #         self._input_values[key] = value
    #
    # def _render_integer(self, element: Element, parent: str) -> None:
    #     key = self.value_key(element, parent)
    #     changed, value = imgui.input_int(
    #         f"{element.name}###{key}",
    #         self._input_values.get(key, 0),
    #     )
    #     assert isinstance(changed, bool)
    #     assert isinstance(value, int)
    #     if changed:
    #         self._input_values[key] = value
    #
    # def _render_floating(self, element: Element, parent: str) -> None:
    #     key = self.value_key(element, parent)
    #     changed, value = imgui.input_float(
    #         f"{element.name}###{key}",
    #         self._input_values.get(key, 0.0),
    #     )
    #     assert isinstance(changed, bool)
    #     assert isinstance(value, float)
    #     if changed:
    #         self._input_values[key] = value
    #
    # def _render_boolean(self, element: Element, parent: str) -> None:
    #     key = self.value_key(element, parent)
    #     changed, value = imgui.checkbox(
    #         f"{element.name}###{key}",
    #         self._input_values.get(key, False),
    #     )
    #     assert isinstance(changed, bool)
    #     assert isinstance(value, bool)
    #     if changed:
    #         self._input_values[key] = value

    # def render_element(self, element: Element, parent: str) -> None:
    #     if isinstance(element.type, ComplexType):
    #         self._render_complex(element, parent)
    #     elif isinstance(element.type, String):
    #         self._render_string(element, parent)
    #     elif isinstance(element.type, Integer):
    #         self._render_integer(element, parent)
    #     elif isinstance(element.type, Float):
    #         self._render_floating(element, parent)
    #     elif isinstance(element.type, Boolean):
    #         self._render_boolean(element, parent)
    #     else:
    #         type_name = type(element.type).__name__
    #         imgui.text(f"Unsupported element type: {type_name}")

    @override
    def on_process(self) -> None:
        self.do_operation()

    def do_operation(self) -> int:
        mishandling = 0
        for name, argument in self._operation.arguments.items():
            if not self.process_argument(argument):
                mishandling += 1
        return mishandling

    def process_argument(self, argument: Argument) -> bool:
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

        handler = self._handlers.get(argument.type_deduction)
        if not handler:
            imgui.text_colored(f"{argument.name} <{typename}>", *self._error_color)
            return False

        handler(argument)
        return True
