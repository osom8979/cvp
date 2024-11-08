# -*- coding: utf-8 -*-

from argparse import Namespace
from inspect import Parameter
from typing import Any, Dict, Final, List, Optional, Tuple

import imgui
from lxml.etree import QName as _EtreeQName
from zeep.xsd import Element
from zeep.xsd.valueobjects import CompoundValue

from cvp.colors.types import RGBA
from cvp.inspect.argument import Argument
from cvp.inspect.member import get_public_instance_attributes, is_private_member
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

    def value_key(self, name: str, parent: str) -> str:
        return f"{parent}{self._element_separator}{name}" if parent else name

    def label_key(self, name: str, parent: str) -> Tuple[str, str]:
        key = self.value_key(name, parent)
        label = f"{name}###{key}"
        return label, key

    @staticmethod
    def tooltip(argument: Argument) -> None:
        if not argument.doc:
            return

        if imgui.is_item_hovered():
            with imgui.begin_tooltip():
                imgui.text(argument.doc)

    def text_error(self, text: str) -> None:
        imgui.text_colored(text, *self._error_color)

    def do_root_argument(self, argument: Argument) -> bool:
        cls = argument.type_deduction()
        try:
            argument.value = self.do_argument(cls, argument)
            return True
        except BaseException as e:
            typename = cls.__name__ if isinstance(cls, type) else str(cls)
            self.text_error(f"{argument.name} <{typename}> {e}")
            return False

    def do_argument(self, cls: Any, argument: Argument) -> Any:
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

    def do_none(self, name: str, value: Any, parent: str) -> None:
        if value == Parameter.empty:
            value = None
        assert value is None
        label, key = self.label_key(name, parent)
        imgui.text(label)
        return None

    def do_boolean(self, name: str, value: Any, parent: str) -> bool:
        if value == Parameter.empty:
            value = False
        assert isinstance(value, bool)
        label, key = self.label_key(name, parent)
        changed, value = imgui.checkbox(label, value)
        assert isinstance(changed, bool)
        assert isinstance(value, bool)
        return value

    def do_integer(self, name: str, value: Any, parent: str) -> int:
        if value == Parameter.empty:
            value = 0
        assert isinstance(value, int)
        label, key = self.label_key(name, parent)
        changed, value = imgui.input_int(label, value)
        assert isinstance(changed, bool)
        assert isinstance(value, int)
        return value

    def do_floating(self, name: str, value: Any, parent: str) -> float:
        if value == Parameter.empty:
            value = 0.0
        assert isinstance(value, float)
        label, key = self.label_key(name, parent)
        changed, value = imgui.input_float(label, value)
        assert isinstance(changed, bool)
        assert isinstance(value, float)
        return value

    def do_string(self, name: str, value: Any, parent: str) -> str:
        if value == Parameter.empty:
            value = str()
        assert isinstance(value, str)
        label, key = self.label_key(name, parent)
        changed, value = imgui.input_text(label, value, INPUT_BUFFER_SIZE)
        assert isinstance(changed, bool)
        assert isinstance(value, str)
        return value

    def do_combo(
        self,
        name: str,
        value: Any,
        parent: str,
        choices: List[str],
    ) -> str:
        assert choices
        if value == Parameter.empty:
            value = choices[0]
        assert isinstance(value, str)
        label, key = self.label_key(name, parent)
        try:
            choice_index = choices.index(value)
        except ValueError:
            choice_index = NOT_FOUND_INDEX
        changed, current = imgui.combo(label, choice_index, choices)
        assert isinstance(changed, bool)
        assert isinstance(current, int)
        return choices[current] if changed else value

    def do_element_annotation(self, argument: Argument, parent: str) -> Any:
        annotation = argument.annotation
        assert isinstance(annotation, ElementAnnotation)
        return self.do_element(
            name=argument.name,
            value=argument.value,
            parent=parent,
            element=annotation.element,
            schema=annotation.schema,
        )

    def do_element(
        self,
        name: str,
        value: Any,
        parent: str,
        element: Element,
        schema: XsdSchema,
    ) -> Any:
        assert isinstance(element.type.accepted_types, list)
        if not element.type.accepted_types:
            return self.do_none(name, None, parent)

        for accepted_type in element.type.accepted_types:
            if not isinstance(accepted_type, type):
                raise TypeError(f"Instances are not supported: {accepted_type}")

            if issubclass(accepted_type, bool):
                return self.do_boolean(name, value, parent)
            elif issubclass(accepted_type, int):
                return self.do_integer(name, value, parent)
            elif issubclass(accepted_type, float):
                return self.do_floating(name, value, parent)
            elif issubclass(accepted_type, str):
                assert isinstance(element.type.qname, _EtreeQName)
                simple_type = schema.simple_types.get(element.type.qname)
                if simple_type is not None:
                    choices = schema.get_enumeration_values(simple_type)
                    if choices:
                        return self.do_combo(name, value, parent, choices)
                return self.do_string(name, value, parent)
            elif issubclass(accepted_type, CompoundValue):
                if value == Parameter.empty:
                    kwargs = self.do_element_kwargs(element, schema, parent)
                    return accepted_type(**kwargs)
                else:
                    return self.do_object(element, value, schema, parent)

        raise TypeError(f"No type is supported: {name}")

    def do_element_kwargs(
        self,
        element: Element,
        schema: XsdSchema,
        parent: str,
    ) -> Dict[str, Any]:
        value = self.do_object(element, Namespace(), schema, parent)
        return {k: v for k, v in get_public_instance_attributes(value)}

    def do_object(
        self,
        element: Element,
        value: object,
        schema: XsdSchema,
        parent: str,
    ) -> object:
        tree_label, tree_key = self.label_key(element.attr_name, parent)
        if imgui.tree_node(tree_label, imgui.TREE_NODE_DEFAULT_OPEN):
            try:
                for child_name, child_element in element.type.elements:
                    assert isinstance(child_name, str)
                    if is_private_member(child_name):
                        continue

                    if isinstance(child_element, Element):
                        if child_element.is_optional:
                            continue

                        item_value = self.do_element(
                            name=child_name,
                            value=getattr(value, child_name, Parameter.empty),
                            parent=tree_key,
                            element=child_element,
                            schema=schema,
                        )
                        setattr(value, child_name, item_value)
                    else:
                        message = f"Unsupported element type: '{child_name}'"
                        self.text_error(message)
                        raise TypeError(message)
            finally:
                imgui.tree_pop()
        return value

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
