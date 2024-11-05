# -*- coding: utf-8 -*-

from typing import Any, Callable, Dict, Final, Optional, Tuple

import imgui

from cvp.colors.types import RGBA
from cvp.inspect.argument import Argument
from cvp.types import override
from cvp.variables import ZEEP_ELEMENT_SEPARATOR
from cvp.widgets.widget import WidgetInterface
from cvp.wsdl.operation import ElementAnnotation, WsdlOperationProxy

# from zeep.xsd.elements.any import Any as ZeepAny
# from zeep.xsd.types.builtins import default_types
# from zeep.xsd.valueobjects import CompoundValue


NOT_FOUND_INDEX: Final[int] = -1
INPUT_BUFFER_SIZE: Final[int] = 2048


class WsdlOperationWidget(WidgetInterface):
    _handlers: Dict[type, Callable[[Argument, Optional[str]], None]]

    def __init__(
        self,
        operation: Optional[WsdlOperationProxy] = None,
        element_separator=ZEEP_ELEMENT_SEPARATOR,
        error_color: Optional[RGBA] = None,
    ):
        self._operation = operation
        self._element_separator = element_separator
        self._error_color = error_color if error_color else 1.0, 0.0, 0.0, 1.0

    def value_key(self, argument_name: str, parent_name: Optional[str] = None) -> str:
        if parent_name:
            return f"{parent_name}{self._element_separator}{argument_name}"
        else:
            return argument_name

    def label_key(
        self,
        argument: Argument,
        parent_name: Optional[str] = None,
    ) -> Tuple[str, str]:
        key = self.value_key(argument.name, parent_name)
        label = f"{argument.name}###{key}"
        return label, key

    @staticmethod
    def tooltip(argument: Argument) -> None:
        if not argument.doc:
            return

        if imgui.is_item_hovered():
            with imgui.begin_tooltip():
                imgui.text(argument.doc)

    def do_argument(self, argument: Argument, parent: Optional[str] = None) -> bool:
        cls = argument.type_deduction
        handler = self.find_handler(cls)
        if not handler:
            typename = cls.__name__ if isinstance(cls, type) else str(cls)
            imgui.text_colored(f"{argument.name} <{typename}>", *self._error_color)
            return False

        handler(argument, parent)
        return True

    def find_handler(self, cls: Any) -> Callable[[Argument, Optional[str]], None]:
        if cls is None:
            return self.do_none

        if isinstance(cls, type):
            if issubclass(cls, str):
                return self.do_string
            elif issubclass(cls, float):
                return self.do_floating
            elif issubclass(cls, int):
                return self.do_integer
            elif issubclass(cls, bool):
                return self.do_boolean
            raise TypeError(f"Cannot find handler for {cls}")

        if isinstance(cls, ElementAnnotation):
            return self.do_element

        raise TypeError(f"Unsupported type: {type(cls).__name__}")

    def do_none(self, argument: Argument, parent: Optional[str] = None) -> None:
        label = self.label_key(argument, parent)[0]
        imgui.text(label)
        self.tooltip(argument)

    def do_string(self, argument: Argument, parent: Optional[str] = None) -> None:
        label = self.label_key(argument, parent)[0]
        # if argument.constraints and argument.constraints.choices:
        #     choices = argument.constraints.choices
        #     choice_value = argument.get_value(choices[0])
        #
        #     try:
        #         choice_index = choices.index(choice_value)
        #     except ValueError:
        #         choice_index = NOT_FOUND_INDEX
        #
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
        # else:
        changed, value = imgui.input_text(
            label,
            argument.get_value(str()),
            INPUT_BUFFER_SIZE,
        )
        self.tooltip(argument)
        assert isinstance(changed, bool)
        assert isinstance(value, str)
        if changed:
            argument.value = value

    def do_floating(self, argument: Argument, parent: Optional[str] = None) -> None:
        label = self.label_key(argument, parent)[0]
        changed, value = imgui.input_float(label, argument.get_value(0.0))
        self.tooltip(argument)
        assert isinstance(changed, bool)
        assert isinstance(value, float)
        if changed:
            argument.value = value

    def do_integer(self, argument: Argument, parent: Optional[str] = None) -> None:
        label = self.label_key(argument, parent)[0]
        changed, value = imgui.input_int(label, argument.get_value(0))
        self.tooltip(argument)
        assert isinstance(changed, bool)
        assert isinstance(value, int)
        if changed:
            argument.value = value

    def do_boolean(self, argument: Argument, parent: Optional[str] = None) -> None:
        label = self.label_key(argument, parent)[0]
        changed, value = imgui.checkbox(label, argument.get_value(False))
        self.tooltip(argument)
        assert isinstance(changed, bool)
        assert isinstance(value, bool)
        if changed:
            argument.value = value

    def do_element(self, argument: Argument, parent: Optional[str] = None) -> None:
        annotation = argument.annotation
        assert isinstance(annotation, ElementAnnotation)
        element = annotation.element
        # schema = annotation.schema

        assert isinstance(element.type.accepted_types, list)
        assert isinstance(element.type.attributes, list)

        # if element.type.qname:
        #     builtin_type = default_types.get(element.type.qname)
        #     if builtin_type is not None:
        #         type_info = builtin_type
        #     elif schema is not None:
        #         type_name = type(element.type).__name__
        #         try:
        #             type_info = schema.get_type(type_name)
        #         except KeyError:
        #             type_info = schema.elements.get(type_name)
        #     else:
        #         type_info = None
        # else:
        #     assert isinstance(element, ZeepAny)
        #     type_info = None

        # if element.type.accepted_types:
        #     primary_accepted_type = element.type.accepted_types[0]
        #     if issubclass(primary_accepted_type, (bool, int, float, str)):
        #         if value == Parameter.empty:
        #             value = primary_accepted_type()
        # else:
        #     primary_accepted_type = Any
        # assert isinstance(primary_accepted_type, type)

        label, key = self.label_key(argument, parent)
        if imgui.tree_node(label, imgui.TREE_NODE_DEFAULT_OPEN):
            # for child_name, child_element in element.type.elements:
            #     self.render_element(child_element, key)
            imgui.tree_pop()

    @override
    def on_process(self) -> None:
        if self._operation is None:
            return

        self.process_operation(self._operation)

    def process_operation(self, operation: WsdlOperationProxy) -> int:
        mishandling = 0
        for argument in operation.arguments.values():
            if not self.do_argument(argument):
                mishandling += 1
        return mishandling
