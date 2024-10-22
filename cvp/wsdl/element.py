# -*- coding: utf-8 -*-

from inspect import Parameter

from zeep.xsd import AnyURI, Boolean, ComplexType, Element, Float, Integer, String

from cvp.inspect.argument import Argument


def element_as_pytype(element: Element) -> type:
    if isinstance(element.type, ComplexType):
        return dict
    elif isinstance(element.type, AnyURI):
        return str
    elif isinstance(element.type, String):
        return str
    elif isinstance(element.type, Integer):
        return int
    elif isinstance(element.type, Float):
        return float
    elif isinstance(element.type, Boolean):
        return bool
    else:
        raise TypeError(f"Unsupported element type: {element.type}")


class BindElement:
    def __init__(self, element: Element):
        self.element = element
        self.argument = Argument.from_details(
            name=element.name,
            kind=Parameter.POSITIONAL_OR_KEYWORD,
            default=element.default_value,
            annotation=element_as_pytype(element),
        )
