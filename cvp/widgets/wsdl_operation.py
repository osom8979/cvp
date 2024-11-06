# -*- coding: utf-8 -*-

from typing import Any, Final, Optional, Tuple

import imgui
from zeep.xsd import Element
from zeep.xsd.types.builtins import QName, default_types
from zeep.xsd.valueobjects import CompoundValue

from cvp.colors.types import RGBA
from cvp.inspect.argument import Argument
from cvp.types import override
from cvp.variables import ZEEP_ELEMENT_SEPARATOR
from cvp.widgets.widget import WidgetInterface
from cvp.wsdl.annotation import ElementAnnotation
from cvp.wsdl.operation import WsdlOperationProxy
from cvp.wsdl.schema import XsdSchema

NOT_FOUND_INDEX: Final[int] = -1
INPUT_BUFFER_SIZE: Final[int] = 2048


class WsdlOperationWidget(WidgetInterface):
    def __init__(
        self,
        operation: Optional[WsdlOperationProxy] = None,
        element_separator=ZEEP_ELEMENT_SEPARATOR,
        error_color: Optional[RGBA] = None,
    ):
        self._operation = operation
        self._element_separator = element_separator
        self._error_color = error_color if error_color else 1.0, 0.0, 0.0, 1.0

    def value_key(self, argument_name: str, parent_name: str) -> str:
        if parent_name:
            return f"{parent_name}{self._element_separator}{argument_name}"
        else:
            return argument_name

    def label_key(self, argument_name: str, parent_name: str) -> Tuple[str, str]:
        key = self.value_key(argument_name, parent_name)
        label = f"{argument_name}###{key}"
        return label, key

    @staticmethod
    def tooltip(argument: Argument) -> None:
        if not argument.doc:
            return

        if imgui.is_item_hovered():
            with imgui.begin_tooltip():
                imgui.text(argument.doc)

    def do_root_argument(self, argument: Argument) -> bool:
        cls = argument.type_deduction()
        try:
            argument.value = self.call_argument_handler(cls, argument)
            return True
        except TypeError:
            typename = cls.__name__ if isinstance(cls, type) else str(cls)
            imgui.text_colored(f"{argument.name} <{typename}>", *self._error_color)
            return False

    def call_argument_handler(self, cls: Any, argument: Argument) -> Any:
        name = argument.name
        parent = str()

        if cls is None:
            return self.do_none(name, None, parent)

        if isinstance(cls, type):
            if issubclass(cls, bool):
                return self.do_boolean(name, argument.get_value(False), parent)
            elif issubclass(cls, int):
                return self.do_integer(name, argument.get_value(0), parent)
            elif issubclass(cls, float):
                return self.do_floating(name, argument.get_value(0.0), parent)
            elif issubclass(cls, str):
                return self.do_string(name, argument.get_value(str()), parent)
            raise TypeError(f"Cannot find handler for {cls}")

        if isinstance(cls, ElementAnnotation):
            return self.do_element_annotation(argument, parent)

        raise TypeError(f"Cannot find handler for {cls}")

    def do_none(self, argument_name: str, value: Any, parent: str) -> Any:
        assert value is None
        label, key = self.label_key(argument_name, parent)
        imgui.text(label)
        return None

    def do_boolean(self, argument_name: str, value: Any, parent: str) -> Any:
        assert isinstance(value, bool)
        label, key = self.label_key(argument_name, parent)
        changed, value = imgui.checkbox(label, value)
        assert isinstance(changed, bool)
        assert isinstance(value, bool)
        return value

    def do_integer(self, argument_name: str, value: Any, parent: str) -> Any:
        assert isinstance(value, int)
        label, key = self.label_key(argument_name, parent)
        changed, value = imgui.input_int(label, value)
        assert isinstance(changed, bool)
        assert isinstance(value, int)
        return value

    def do_floating(self, argument_name: str, value: Any, parent: str) -> Any:
        assert isinstance(value, float)
        label, key = self.label_key(argument_name, parent)
        changed, value = imgui.input_float(label, value)
        assert isinstance(changed, bool)
        assert isinstance(value, float)
        return value

    def do_string(self, argument_name: str, value: Any, parent: str) -> Any:
        assert isinstance(value, str)
        label, key = self.label_key(argument_name, parent)
        changed, value = imgui.input_text(label, value, INPUT_BUFFER_SIZE)
        assert isinstance(changed, bool)
        assert isinstance(value, str)
        return value

    def do_combo(self, argument: Argument, value: Any, parent: str) -> Any:
        assert isinstance(value, str)
        label, key = self.label_key(argument.name, parent)
        # if argument.constraints and argument.constraints.choices:
        #     choices = argument.constraints.choices
        #     choice_value = argument.get_value(choices[0])
        #     try:
        #         choice_index = choices.index(choice_value)
        #     except ValueError:
        #         choice_index = NOT_FOUND_INDEX
        #     changed, value = imgui.combo(
        #         label,
        #         choice_index,
        #         choices,
        #     )
        #     self.tooltip(argument)
        #     assert isinstance(changed, bool)
        #     assert isinstance(value, int)
        #     if changed:
        #         argument.value = choices[value]

    def do_element_annotation(self, argument: Argument, parent: str) -> Any:
        annotation = argument.annotation
        assert isinstance(annotation, ElementAnnotation)
        name = argument.name
        element = annotation.element
        schema = annotation.schema

        # assert isinstance(element.type.qname, QName)
        # simple_type = schema.simple_types.get(element.type.qname)
        # element_type = schema.elements.get(element.type.qname)
        # builtin_type = default_types.get(element.type.qname)

        assert isinstance(element.type.accepted_types, list)
        if not element.type.accepted_types:
            return self.do_none(name, None, parent)

        for accepted_type in element.type.accepted_types:
            if not isinstance(accepted_type, type):
                raise TypeError(f"Instances are not supported: {accepted_type}")

            if issubclass(accepted_type, bool):
                return self.do_boolean(name, argument.get_value(False), parent)
            elif issubclass(accepted_type, int):
                return self.do_integer(name, argument.get_value(0), parent)
            elif issubclass(accepted_type, float):
                return self.do_floating(name, argument.get_value(0.0), parent)
            elif issubclass(accepted_type, str):
                return self.do_string(name, argument.get_value(str()), parent)
            elif issubclass(accepted_type, CompoundValue):
                return accepted_type(**self.do_element(element, schema, parent))

        raise TypeError(f"No type is supported: {annotation.name}")

    def do_element(
        self,
        element: Element,
        schema: XsdSchema,
        parent: str,
    ) -> Any:
        # assert isinstance(element.type.qname, QName)
        # complex_type = schema.complex_types[element.type.qname]
        label, key = self.label_key(element.attr_name, parent)

        result = dict()
        if imgui.tree_node(label, imgui.TREE_NODE_DEFAULT_OPEN):
            for child_name, child_element in element.type.elements:
                assert isinstance(child_name, str)
                assert isinstance(child_element, Element)
                # result[child_name] = self.do_element(child_element, schema, key)
            imgui.tree_pop()
        return result

    @override
    def on_process(self) -> None:
        if self._operation is None:
            return

        self.process_operation(self._operation)

    def process_operation(self, operation: WsdlOperationProxy) -> int:
        mishandling = 0
        for argument in operation.arguments.values():
            if not self.do_root_argument(argument):
                mishandling += 1
        return mishandling
