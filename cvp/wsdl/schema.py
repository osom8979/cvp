# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Dict, Final, List
from urllib.parse import urljoin, urlparse

from lxml import etree
from zeep.transports import Transport

# noinspection PyProtectedMember
_EtreeElement = etree._Element
_NamespaceKey = str
_UrlKey = str
_XmlNs = str

XSD_NS: Final[str] = "xs"
XSD_URL: Final[str] = "http://www.w3.org/2001/XMLSchema"


class XsdSchema:
    _loaded: Dict[_UrlKey, _EtreeElement]
    _prefixes: Dict[_XmlNs, _NamespaceKey]
    _simple_types: Dict[str, _EtreeElement]
    _complex_types: Dict[str, _EtreeElement]

    def __init__(self, location: str, transport: Transport):
        self._loaded = dict()
        self._prefixes = dict()
        self._simple_types = dict()
        self._complex_types = dict()
        self._types = dict()

        self._tree = OrderedDict[_NamespaceKey, _EtreeElement]()
        self._root_location = location
        self._transport = transport
        self._parser = etree.XMLParser(remove_comments=True)

        data = self._transport.load(location)
        if not data:
            raise ValueError("There is no schema data")

        self._root = etree.XML(data, self._parser)
        if self._root is None:
            raise ValueError("Schema element could not be read")

        target_namespace = self._root.attrib.get("targetNamespace")
        self._tree[target_namespace] = self._root

        self._process_element(self._root)

        for prefix, namespace in self._root.nsmap.items():
            assert isinstance(prefix, _XmlNs)
            assert isinstance(namespace, _NamespaceKey)
            self._prefixes[prefix] = namespace

        for node in self._tree.values():
            for e in self.get_simple_types(node):
                name = e.get("name")
                assert isinstance(name, str)
                self._simple_types[name] = e
                self._types[name] = e
            for e in self.get_complex_types(node):
                name = e.get("name")
                assert isinstance(name, str)
                self._complex_types[name] = e
                self._types[name] = e

    @property
    def root(self):
        return self._root

    @property
    def namespaces(self):
        return self._tree.keys()

    @property
    def prefixes(self):
        return self._prefixes

    @property
    def simple_types(self):
        return self._simple_types

    @property
    def complex_types(self):
        return self._complex_types

    @property
    def types(self):
        return self._types

    @staticmethod
    def get_simple_types(node: _EtreeElement, ns=XSD_URL):
        return node.iterchildren(f"{{{ns}}}simpleType")

    @staticmethod
    def get_complex_types(node: _EtreeElement, ns=XSD_URL):
        return node.iterchildren(f"{{{ns}}}complexType")

    @staticmethod
    def is_url(url: str) -> bool:
        try:
            result = urlparse(url)
            return all((result.scheme, result.netloc))
        except ValueError:
            return False

    def resolve_url(self, location: str) -> str:
        if self.is_url(location):
            return location
        else:
            return urljoin(urljoin(self._root_location, "."), location)

    def load(self, location: str):
        url = self.resolve_url(location)
        if url in self._loaded:
            raise KeyError(f"Already loaded url: '{url}'")

        data = self._transport.load(url)
        node = etree.XML(data, self._parser)
        self._loaded[url] = node
        return node

    def _process_element(self, parent: _EtreeElement):
        self._process_includes(parent)
        self._process_imports(parent)

    def _process_includes(self, parent: _EtreeElement, ns=XSD_URL):
        for node in parent.iterchildren(f"{{{ns}}}include"):
            assert isinstance(node, _EtreeElement)
            schema_location = node.attrib.get("schemaLocation")
            if not schema_location:
                continue

            try:
                child = self.load(schema_location)
            except KeyError:
                continue

            self._process_element(child)
            if child.tag != f"{{{ns}}}schema":
                continue

            for elem in child.getchildren():
                assert isinstance(elem, _EtreeElement)
                parent.append(elem)

    def _process_imports(self, parent: _EtreeElement, ns=XSD_URL):
        for node in parent.iterchildren(f"{{{ns}}}import"):
            assert isinstance(node, _EtreeElement)
            namespace = node.attrib.get("namespace")
            schema_location = node.attrib.get("schemaLocation")
            if not namespace or not schema_location:
                continue

            try:
                child = self.load(schema_location)
            except KeyError:
                continue

            self._process_element(child)
            if child.tag != f"{{{ns}}}schema":
                continue

            self._tree[namespace] = child
            self._process_element(child)

    @staticmethod
    def enumerations_xpath(name: str, xs=XSD_NS) -> str:
        return f"//{xs}:simpleType[@name='{name}']/{xs}:restriction/{xs}:enumeration"

    def get_enumerations(self, simple_type: str, xs=XSD_NS, xsns=XSD_URL) -> List[str]:
        xpath = self.enumerations_xpath(simple_type, xs)
        enumerations = self.root.xpath(xpath, namespaces={xs: xsns})
        return [enum.get("value") for enum in enumerations]
