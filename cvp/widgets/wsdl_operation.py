# -*- coding: utf-8 -*-

from typing import Callable, Dict, Final, Optional, Tuple

import imgui
from zeep.xsd.valueobjects import CompoundValue

from cvp.colors.types import RGBA
from cvp.inspect.argument import Argument
from cvp.types import override
from cvp.variables import ZEEP_ELEMENT_SEPARATOR
from cvp.widgets.widget import WidgetInterface
from cvp.wsdl.operation import WsdlOperationProxy

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

    def find_handler(self, cls: type) -> Callable[[Argument, Optional[str]], None]:
        if issubclass(cls, CompoundValue):
            return self.do_compound_value
        elif issubclass(cls, str):
            return self.do_string
        elif issubclass(cls, float):
            return self.do_floating
        elif issubclass(cls, int):
            return self.do_integer
        elif issubclass(cls, bool):
            return self.do_boolean
        raise TypeError(f"Cannot find handler for {cls}")

    def do_argument(self, argument: Argument, parent: Optional[str] = None) -> bool:
        assert not argument.is_empty_annotation
        assert argument.is_annotated

        arg_type = argument.type_deduction
        typename = arg_type.__name__ if isinstance(arg_type, type) else str(arg_type)
        assert isinstance(typename, str)

        handler = self.find_handler(arg_type)
        if not handler:
            imgui.text_colored(f"{argument.name} <{typename}>", *self._error_color)
            return False

        handler(argument, parent)
        return True

    def do_boolean(self, argument: Argument, parent: Optional[str] = None) -> None:
        label = self.label_key(argument, parent)[0]
        changed, value = imgui.checkbox(label, argument.get_value(False))
        self.tooltip(argument)
        assert isinstance(changed, bool)
        assert isinstance(value, bool)
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

    def do_floating(self, argument: Argument, parent: Optional[str] = None) -> None:
        label = self.label_key(argument, parent)[0]
        changed, value = imgui.input_float(label, argument.get_value(0.0))
        self.tooltip(argument)
        assert isinstance(changed, bool)
        assert isinstance(value, float)
        if changed:
            argument.value = value

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

    def do_compound_value(
        self,
        argument: Argument,
        parent: Optional[str] = None,
    ) -> None:
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
