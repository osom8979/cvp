# -*- coding: utf-8 -*-

from typing import Any, Final, List, Optional, Tuple

import imgui
from zeep.wsdl.definitions import Operation
from zeep.xsd import Boolean, ComplexType, Element, Float, Integer, String

from cvp.types import override
from cvp.variables import ZEEP_ELEMENT_SEPARATOR
from cvp.widgets.widget import WidgetInterface

INPUT_BUFFER_SIZE: Final[int] = 2048


class WsdlOperationWidget(WidgetInterface):
    def __init__(
        self,
        operation: Operation,
        element_separator: Optional[str] = ZEEP_ELEMENT_SEPARATOR,
        **input_values: Any,
    ):
        self._operation = operation
        self._element_separator = element_separator
        self._input_values = input_values

    @property
    def name(self) -> str:
        # noinspection PyProtectedMember
        return self._operation.name

    @property
    def input(self):
        # noinspection PyUnresolvedReferences
        return self._operation.input  # type: ignore[attr-defined]

    @property
    def input_elements(self) -> List[Tuple[str, Element]]:
        try:
            return self.input.body.type.elements
        except AttributeError:
            return list()

    def render_input_elements(self) -> None:
        for name, element in self.input_elements:
            self.render_root_elements(element)

    def render_root_elements(self, element: Element) -> None:
        self.render_element(element, str())

    def value_key(self, element: Element, parent: str) -> str:
        return f"{parent}{self._element_separator}{element.name}"

    def _render_complex(self, element: Element, parent: str) -> None:
        key = self.value_key(element, parent)
        if imgui.tree_node(f"{element.name}###{key}", imgui.TREE_NODE_DEFAULT_OPEN):
            for child_name, child_element in element.type.elements:
                self.render_element(child_element, key)
            imgui.tree_pop()

    def _render_string(self, element: Element, parent: str) -> None:
        key = self.value_key(element, parent)
        changed, value = imgui.input_text(
            f"{element.name}###{key}",
            self._input_values.get(key, str()),
            INPUT_BUFFER_SIZE,
        )
        assert isinstance(changed, bool)
        assert isinstance(value, str)
        if changed:
            self._input_values[key] = value

    def _render_integer(self, element: Element, parent: str) -> None:
        key = self.value_key(element, parent)
        changed, value = imgui.input_int(
            f"{element.name}###{key}",
            self._input_values.get(key, 0),
        )
        assert isinstance(changed, bool)
        assert isinstance(value, int)
        if changed:
            self._input_values[key] = value

    def _render_floating(self, element: Element, parent: str) -> None:
        key = self.value_key(element, parent)
        changed, value = imgui.input_float(
            f"{element.name}###{key}",
            self._input_values.get(key, 0.0),
        )
        assert isinstance(changed, bool)
        assert isinstance(value, float)
        if changed:
            self._input_values[key] = value

    def _render_boolean(self, element: Element, parent: str) -> None:
        key = self.value_key(element, parent)
        changed, value = imgui.checkbox(
            f"{element.name}###{key}",
            self._input_values.get(key, False),
        )
        assert isinstance(changed, bool)
        assert isinstance(value, bool)
        if changed:
            self._input_values[key] = value

    def render_element(self, element: Element, parent: str) -> None:
        if isinstance(element.type, ComplexType):
            self._render_complex(element, parent)
        elif isinstance(element.type, String):
            self._render_string(element, parent)
        elif isinstance(element.type, Integer):
            self._render_integer(element, parent)
        elif isinstance(element.type, Float):
            self._render_floating(element, parent)
        elif isinstance(element.type, Boolean):
            self._render_boolean(element, parent)
        else:
            type_name = type(element.type).__name__
            imgui.text(f"Unsupported element type: {type_name}")

    @override
    def on_process(self) -> None:
        self.render_input_elements()
