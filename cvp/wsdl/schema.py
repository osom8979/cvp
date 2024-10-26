# -*- coding: utf-8 -*-

from typing import Any, Dict, List

from lxml import etree
from zeep.transports import Transport
from zeep.xsd import Schema
from zeep.xsd.elements.base import Base as BaseElement
from zeep.xsd.elements.builtins import Schema as SchemaElement
from zeep.xsd.elements.element import Element
from zeep.xsd.schema import SchemaDocument


class XsdSchema:
    def __init__(self, location: str, transport: Transport):
        data = transport.load(location)
        if not data:
            raise ValueError("There is no schema data")

        parser = etree.XMLParser(remove_comments=True)
        self._root = etree.XML(data, parser)
        if self._root is None:
            raise ValueError("Schema element could not be read")

        self._schema = Schema(self._root, transport, location)
        for prefix, namespace in self._root.nsmap.items():
            assert isinstance(prefix, str)
            assert isinstance(namespace, str)
            self._schema.set_ns_prefix(prefix, namespace)

    @property
    def root(self):
        return self._root

    @property
    def namespaces(self) -> List[str]:
        return self._schema.namespaces

    @property
    def prefix_map(self) -> Dict[str, str]:
        return self._schema.prefix_map

    @property
    def documents(self) -> List[SchemaDocument]:
        return [d for d in self._schema.documents.values()]

    @property
    def types(self) -> Dict[str, Any]:
        return {type(t).__name__: t for t in self._schema.types}

    @property
    def elements(self) -> List[BaseElement]:
        result = list(self._schema.elements)
        assert isinstance(result[0], SchemaElement)
        for element in result[1:]:
            assert isinstance(element, Element)
        return result
