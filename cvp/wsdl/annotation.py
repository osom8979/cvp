# -*- coding: utf-8 -*-

from typing import Any, Union

from zeep.xsd import Element
from zeep.xsd.elements.any import Any as ZeepAny
from zeep.xsd.types.builtins import QName, default_types

from cvp.wsdl.schema import XsdSchema


class ElementAnnotation:
    def __init__(self, element: Element, schema: XsdSchema):
        self.element = element
        self.schema = schema

    @property
    def accepts_multiple(self) -> bool:
        return self.element.accepts_multiple

    @property
    def attr_name(self) -> str:
        return self.element.attr_name

    @property
    def name(self) -> str:
        return self.element.name

    @property
    def default(self) -> Any:
        return self.element.default

    @property
    def default_value(self) -> Any:
        return self.element.default_value

    @property
    def is_global(self) -> bool:
        return self.element.is_global

    @property
    def is_optional(self) -> bool:
        return self.element.is_global

    @property
    def min_occurs(self) -> Union[str, int]:
        return self.element.min_occurs

    @property
    def max_occurs(self) -> Union[str, int]:
        return self.element.max_occurs

    @property
    def nillable(self) -> bool:
        return self.element.nillable

    @property
    def qname(self) -> QName:
        return self.element.qname

    @property
    def type_accepted_types(self):
        assert isinstance(self.element.type.accepted_types, list)
        return self.element.type.accepted_types

    @property
    def type_attributes(self):
        assert isinstance(self.element.type.attributes, list)
        return self.element.type.attributes

    @property
    def type_is_global(self) -> bool:
        return self.element.type.is_global

    @property
    def type_name(self) -> str:
        return self.element.type.name

    @property
    def type_qname(self) -> QName:
        return self.element.type.qname

    @property
    def is_any_type(self) -> bool:
        if not self.type_qname:
            assert isinstance(self.element, ZeepAny)
            return True
        else:
            return False

    @property
    def is_builtin_type(self) -> bool:
        return default_types.get(self.type_qname) is not None

    @property
    def is_complex(self) -> bool:
        return self.type_qname in self.schema.complex_types

    @property
    def is_simple(self) -> bool:
        return self.type_qname in self.schema.simple_types
