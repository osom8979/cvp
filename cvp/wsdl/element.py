# -*- coding: utf-8 -*-

from zeep.xsd import AnyURI, Boolean, ComplexType, Element, Float, Integer, String

from cvp.inspect.argument import ParamType


def element_as_ptype(element: Element) -> ParamType:
    if isinstance(element.type, ComplexType):
        return ParamType.mapping
    elif isinstance(element.type, AnyURI):
        return ParamType.uri
    elif isinstance(element.type, String):
        return ParamType.string
    elif isinstance(element.type, Integer):
        return ParamType.integer
    elif isinstance(element.type, Float):
        return ParamType.floating
    elif isinstance(element.type, Boolean):
        return ParamType.boolean
    else:
        raise TypeError(f"Unsupported element type: {element.type}")
