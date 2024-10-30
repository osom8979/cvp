# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Dict, Final, List, Optional, TypeAlias, Union
from urllib.parse import urljoin, urlparse

from lxml import etree
from lxml.etree import QName
from zeep.transports import Transport

# noinspection PyProtectedMember
from lxml.etree import _Element as _EtreeElement  # isort:skip

_NamespaceKey: TypeAlias = str
_UrlKey: TypeAlias = str
_XmlNs: TypeAlias = str

XSD_NS: Final[str] = "xs"
XSD_URL: Final[str] = "http://www.w3.org/2001/XMLSchema"


class XsdSchema:
    _loaded: Dict[_UrlKey, _EtreeElement]
    _prefixes: Dict[_XmlNs, _NamespaceKey]
    _simple_types: Dict[QName, _EtreeElement]
    _complex_types: Dict[QName, _EtreeElement]
    _types: Dict[QName, _EtreeElement]
    _names: Dict[str, _EtreeElement]

    def __init__(
        self,
        location: str,
        transport: Transport,
        *,
        root: Optional[_EtreeElement] = None,
    ):
        self._loaded = dict()
        self._prefixes = dict()
        self._simple_types = dict()
        self._complex_types = dict()
        self._types = dict()
        self._names = dict()

        self._tree = OrderedDict[_NamespaceKey, _EtreeElement]()
        self._root_location = location
        self._transport = transport
        self._parser = etree.XMLParser(remove_comments=True)

        if root is None:
            data = self._transport.load(location)
            if not data:
                raise ValueError("There is no schema data")
            root = etree.XML(data, self._parser)

        if root is None:
            raise ValueError("Schema element could not be read")

        target_namespace = root.attrib.get("targetNamespace")
        assert isinstance(target_namespace, str)
        assert target_namespace

        self._root = root
        self._root_namespace = target_namespace
        self._process_element(root)
        self.insert(target_namespace, root)

    @property
    def root(self) -> _EtreeElement:
        return self._root

    @property
    def root_namespace(self):
        return self._root_namespace

    @property
    def root_prefix(self):
        for prefix, namespace in self._prefixes.items():
            if namespace == self._root_namespace:
                return prefix
        raise IndexError(f"Not found root prefix: '{self._root_namespace}'")

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

    @property
    def names(self):
        return self._names

    @staticmethod
    def _get_simple_types(node: _EtreeElement, *, ns=XSD_URL) -> List[_EtreeElement]:
        return list(node.iterchildren(f"{{{ns}}}simpleType"))

    @staticmethod
    def _get_complex_types(node: _EtreeElement, *, ns=XSD_URL) -> List[_EtreeElement]:
        return list(node.iterchildren(f"{{{ns}}}complexType"))

    @staticmethod
    def _is_url(url: str) -> bool:
        try:
            result = urlparse(url)
            return all((result.scheme, result.netloc))
        except ValueError:
            return False

    def resolve_url(self, location: str) -> str:
        if self._is_url(location):
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

    def _process_element(self, parent: _EtreeElement, *, ns=XSD_URL):
        self._process_includes(parent, ns=ns)
        self._process_imports(parent, ns=ns)
        self._process_nsmap(parent, ns=ns)

    def _process_includes(self, parent: _EtreeElement, *, ns=XSD_URL):
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

    def _process_imports(self, parent: _EtreeElement, *, ns=XSD_URL):
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

            self.insert(namespace, child)

    def _process_nsmap(self, parent: _EtreeElement, *, ns=XSD_URL):
        if parent.tag != f"{{{ns}}}schema":
            return

        for prefix, namespace in parent.nsmap.items():
            if prefix is None:
                prefix = self._gen_prefix()
            assert isinstance(prefix, _XmlNs)
            assert isinstance(namespace, _NamespaceKey)
            self._prefixes[prefix] = namespace

    def _gen_prefix(self, *, prefix="ns", index=0) -> _XmlNs:
        candidate_prefix = f"{prefix}{index}"
        for ns in self._prefixes.keys():
            if candidate_prefix == ns:
                index += 1
                candidate_prefix = f"{prefix}{index}"
        return candidate_prefix

    def insert(self, namespace: str, node: _EtreeElement) -> None:
        self._tree[namespace] = node

        for e in self._get_simple_types(node):
            name = e.get("name")
            if not name:
                continue
            assert isinstance(name, str)
            qname = QName(f"{{{namespace}}}{name}")
            self._simple_types[qname] = e
            self._types[qname] = e
            self._names[qname.localname] = e

        for e in self._get_complex_types(node):
            name = e.get("name")
            if not name:
                continue
            assert isinstance(name, str)
            qname = QName(f"{{{namespace}}}{name}")
            self._complex_types[qname] = e
            self._types[qname] = e
            self._names[qname.localname] = e

    def get_type(self, name: Union[str, QName]) -> _EtreeElement:
        if isinstance(name, QName):
            qname = name
        elif isinstance(name, str):
            try:
                qname = QName(name)
            except ValueError:
                if name.find(":") == -1:
                    raise
                prefix, localname = name.split(":", 1)
                qname = QName(f"{{{self._prefixes[prefix]}}}{localname}")
        else:
            raise TypeError(f"Unexpected type: {type(name).__name__}")

        if not qname.namespace:
            return self._names[qname.localname]

        if not self._is_url(qname.namespace):
            qname.namespace = self._prefixes[qname.namespace]

        return self._types[qname]

    def __getitem__(self, item):
        return self.get_type(item)

    def get_root_type(self, localname: str) -> _EtreeElement:
        return self.get_type(f"{{{self._root_namespace}}}{localname}")

    @staticmethod
    def get_restriction(node: _EtreeElement, *, ns=XSD_URL) -> List[_EtreeElement]:
        return list(node.iterchildren(f"{{{ns}}}restriction"))

    @staticmethod
    def get_enumeration(node: _EtreeElement, *, ns=XSD_URL) -> List[_EtreeElement]:
        restriction = XsdSchema.get_restriction(node, ns=ns)[0]
        return list(restriction.iterchildren(f"{{{ns}}}enumeration"))

    @staticmethod
    def get_enumeration_values(node: _EtreeElement, *, ns=XSD_URL) -> List[str]:
        enumerations = XsdSchema.get_enumeration(node, ns=ns)
        return list(e.get("value") for e in enumerations)
