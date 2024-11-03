# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Dict, Final, List, Optional, Tuple, TypeAlias, Union
from urllib.parse import urljoin, urlparse

from lxml import etree
from lxml.etree import QName
from zeep.transports import Transport
from zeep.xsd.types.builtins import default_types as _zeep_default_types

# noinspection PyProtectedMember
from lxml.etree import _Element as _EtreeElement  # isort:skip

_Namespace: TypeAlias = str
_Prefix: TypeAlias = str
_UrlKey: TypeAlias = str
_LocalName: TypeAlias = str

XSD_PREFIX: Final[str] = "xs"
XSD_NAMESPACE: Final[str] = "http://www.w3.org/2001/XMLSchema"


class XsdSchema:
    DefaultTypes = _zeep_default_types

    _loaded: Dict[_UrlKey, _EtreeElement]
    _prefixes: Dict[_Prefix, _Namespace]
    _simple_types: Dict[QName, _EtreeElement]
    _complex_types: Dict[QName, _EtreeElement]
    _elements: Dict[QName, _EtreeElement]
    _types: Dict[QName, _EtreeElement]
    _names: Dict[_LocalName, _EtreeElement]
    _tree: OrderedDict[_Namespace, _EtreeElement]

    _location: str
    _transport: Transport
    _xsd_prefix: _Prefix
    _xsd_namespace: _Namespace

    _root_element: _EtreeElement
    _root_namespace: _Namespace
    _root_prefix: _Prefix

    def __init__(
        self,
        location: str,
        transport: Optional[Transport] = None,
        *,
        root: Optional[_EtreeElement] = None,
        base_location: Optional[str] = None,
        xsd_prefix=XSD_PREFIX,
        xsd_namespace=XSD_NAMESPACE,
        parser: Optional[etree.XMLParser] = None,
    ):
        self._loaded = dict()
        self._prefixes = dict()
        self._simple_types = dict()
        self._complex_types = dict()
        self._elements = dict()
        self._types = dict()
        self._names = dict()
        self._tree = OrderedDict()

        self._location = location
        self._transport = transport if transport else Transport()
        self._xsd_prefix = xsd_prefix
        self._xsd_namespace = xsd_namespace
        self._prefixes[xsd_prefix] = xsd_namespace

        self._parser = parser if parser else etree.XMLParser(remove_comments=True)

        if root is None:
            data = self._transport.load(location)
            if not data:
                raise ValueError("There is no schema data")
            root = etree.XML(data, self._parser)

        if root is None:
            raise ValueError("Schema element could not be read")

        if root.tag != f"{{{xsd_namespace}}}schema":
            raise ValueError("The root must be an XSD schema tag")

        target_namespace = root.attrib.get("targetNamespace")
        if not target_namespace:
            raise ValueError("Not found 'targetNamespace' attribute")

        assert isinstance(target_namespace, str)
        assert target_namespace

        try:
            root_prefix = self._find_prefix(root, target_namespace)
        except IndexError:
            root_prefix = self.generate_prefix_name()

        self._root_element = root
        self._root_namespace = target_namespace
        self._root_prefix = root_prefix
        self._prefixes[root_prefix] = target_namespace

        if not base_location:
            base_location = urljoin(location, ".")
        assert isinstance(base_location, str)
        assert base_location
        self._base_location = base_location

        self._process_element(root, base_location)
        self._insert_node(target_namespace, root)

    @classmethod
    def from_target_namespace(
        cls,
        location: str,
        transport: Optional[Transport] = None,
        target_namespace: Optional[Union[int, str]] = None,
        *,
        base_location: Optional[str] = None,
        xsd_prefix=XSD_PREFIX,
        xsd_namespace=XSD_NAMESPACE,
        parser: Optional[etree.XMLParser] = None,
    ):
        if not transport:
            transport = Transport()
        assert transport is not None
        assert isinstance(transport, Transport)

        data = transport.load(location)
        if not data:
            raise ValueError("There is no schema data")

        if not parser:
            parser = etree.XMLParser(remove_comments=True)
        assert parser is not None
        assert isinstance(parser, etree.XMLParser)

        root = etree.XML(data, parser)
        namespaces = {xsd_prefix: xsd_namespace}
        schemas = list(root.xpath(f"//{xsd_prefix}:schema", namespaces=namespaces))
        if not schemas:
            raise ValueError("Not found schema element")

        if target_namespace is None:
            root_node = schemas[0]
        elif isinstance(target_namespace, int):
            root_node = schemas[target_namespace]
        else:
            assert isinstance(target_namespace, str)
            root_node = None
            for e in schemas:
                assert isinstance(e, _EtreeElement)
                if target_namespace == e.attrib.get("targetNamespace"):
                    root_node = e
                    break
            if root_node is None:
                raise ValueError(f"Not found target namespace: '{target_namespace}'")

        return cls(
            location,
            transport,
            root=root_node,
            base_location=base_location,
            xsd_prefix=xsd_prefix,
            xsd_namespace=xsd_namespace,
            parser=parser,
        )

    @property
    def root_element(self) -> _EtreeElement:
        return self._root_element

    @property
    def root_namespace(self):
        return self._root_namespace

    @property
    def root_prefix(self):
        return self._root_prefix

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
    def elements(self):
        return self._elements

    @property
    def types(self):
        return self._types

    @property
    def names(self):
        return self._names

    def xsd_qname(self, name: str) -> str:
        return "{" + self._xsd_namespace + "}" + name

    def xsd_tag(self, name: str) -> str:
        return self._xsd_prefix + ":" + name

    @property
    def xsd_nsmap(self) -> Dict[str, str]:
        return {self._xsd_prefix: self._xsd_namespace}

    @property
    def xsd_simple_type(self) -> str:
        return self.xsd_qname("simpleType")

    @property
    def xsd_complex_type(self) -> str:
        return self.xsd_qname("complexType")

    @property
    def xsd_include(self) -> str:
        return self.xsd_qname("include")

    @property
    def xsd_import(self) -> str:
        return self.xsd_qname("import")

    @property
    def xsd_schema(self) -> str:
        return self.xsd_qname("schema")

    @property
    def xsd_restriction(self) -> str:
        return self.xsd_qname("restriction")

    @property
    def xsd_enumeration(self) -> str:
        return self.xsd_qname("enumeration")

    def get_schemas(
        self,
        node: _EtreeElement,
        *,
        skip_error=False,
    ) -> List[Tuple[str, _EtreeElement]]:
        result = list()
        xpath = "//" + self.xsd_tag("schema")
        for e in node.xpath(xpath, namespaces=self.xsd_nsmap):
            assert isinstance(e, _EtreeElement)

            target_namespace = e.attrib.get("targetNamespace")
            if not target_namespace:
                if skip_error:
                    continue
                raise ValueError("Not found 'targetNamespace' attribute")

            assert isinstance(target_namespace, str)
            assert target_namespace

            result.append((target_namespace, e))
        return result

    def get_simple_types(
        self,
        node: _EtreeElement,
        *,
        strip_noname=True,
    ) -> List[Tuple[str, _EtreeElement]]:
        result = list()
        xpath = "//" + self.xsd_tag("simpleType")
        for e in node.xpath(xpath, namespaces=self.xsd_nsmap):
            assert isinstance(e, _EtreeElement)
            name = e.get("name")
            if not name and strip_noname:
                continue
            assert isinstance(name, str)
            result.append((name, e))
        return result

    def get_complex_types(
        self,
        node: _EtreeElement,
        *,
        strip_noname=True,
    ) -> List[Tuple[str, _EtreeElement]]:
        result = list()
        xpath = "//" + self.xsd_tag("complexType")
        for e in node.xpath(xpath, namespaces=self.xsd_nsmap):
            assert isinstance(e, _EtreeElement)
            name = e.get("name")
            if not name and strip_noname:
                continue
            assert isinstance(name, str)
            result.append((name, e))
        return result

    def get_elements(
        self,
        node: _EtreeElement,
        *,
        strip_noname=True,
    ) -> List[Tuple[str, _EtreeElement]]:
        result = list()
        xpath = "//" + self.xsd_tag("element")
        for e in node.xpath(xpath, namespaces=self.xsd_nsmap):
            assert isinstance(e, _EtreeElement)
            name = e.get("name")
            if not name and strip_noname:
                continue
            assert isinstance(name, str)
            result.append((name, e))
        return result

    @staticmethod
    def _is_url(url: str) -> bool:
        try:
            result = urlparse(url)
            return all((result.scheme, result.netloc))
        except ValueError:
            return False

    @staticmethod
    def _find_prefix(node: _EtreeElement, namespace: str) -> str:
        for prefix, ns in node.nsmap.items():
            if namespace == ns:
                return prefix
        raise IndexError(f"Not found namespace prefix: '{namespace}'")

    def resolve_url(self, location: str, base_location: Optional[str] = None) -> str:
        if self._is_url(location):
            return location
        else:
            # 'location' is relative path.
            if base_location:
                return urljoin(base_location, location)
            else:
                return urljoin(self._base_location, location)

    def load(self, url: str) -> _EtreeElement:
        if url in self._loaded:
            raise KeyError(f"Already loaded url: '{url}'")

        data = self._transport.load(url)
        node = etree.XML(data, self._parser)
        self._loaded[url] = node
        return node

    def _process_element(self, parent: _EtreeElement, base_location: str) -> None:
        self._process_includes(parent, base_location)
        self._process_imports(parent, base_location)
        self._process_nsmap(parent)

    def _process_includes(self, parent: _EtreeElement, base_location: str) -> None:
        for node in parent.iterchildren(self.xsd_include):
            assert isinstance(node, _EtreeElement)
            schema_location = node.attrib.get("schemaLocation")
            if not schema_location:
                continue

            schema_url = self.resolve_url(schema_location, base_location)
            schema_base = urljoin(schema_url, ".")

            try:
                child = self.load(schema_url)
            except KeyError:
                continue

            self._process_element(child, schema_base)
            if child.tag != self.xsd_schema:
                continue

            for elem in child.getchildren():
                assert isinstance(elem, _EtreeElement)
                parent.append(elem)

    def _process_imports(self, parent: _EtreeElement, base_location: str) -> None:
        for node in parent.iterchildren(self.xsd_import):
            assert isinstance(node, _EtreeElement)
            namespace = node.attrib.get("namespace")
            schema_location = node.attrib.get("schemaLocation")
            if not namespace or not schema_location:
                continue

            schema_url = self.resolve_url(schema_location, base_location)
            schema_base = urljoin(schema_url, ".")

            try:
                child = self.load(schema_url)
            except KeyError:
                continue

            self._process_element(child, schema_base)
            if child.tag != self.xsd_schema:
                continue

            self._insert_node(namespace, child)

    def _process_nsmap(self, parent: _EtreeElement):
        if parent.tag != self.xsd_schema:
            return

        for prefix, namespace in parent.nsmap.items():
            if prefix is None:
                prefix = self.generate_prefix_name()
            assert isinstance(prefix, _Prefix)
            assert isinstance(namespace, _Namespace)
            self._prefixes[prefix] = namespace

    def generate_prefix_name(self, *, prefix="ns", index=0) -> _Prefix:
        candidate_prefix = f"{prefix}{index}"
        for ns in self._prefixes.keys():
            if candidate_prefix == ns:
                index += 1
                candidate_prefix = f"{prefix}{index}"
        return candidate_prefix

    def _insert_node(self, namespace: str, node: _EtreeElement) -> None:
        self._tree[namespace] = node

        for name, e in self.get_simple_types(node):
            qname = QName(f"{{{namespace}}}{name}")
            self._simple_types[qname] = e
            self._types[qname] = e
            self._names[qname.localname] = e

        for name, e in self.get_complex_types(node):
            qname = QName(f"{{{namespace}}}{name}")
            self._complex_types[qname] = e
            self._types[qname] = e
            self._names[qname.localname] = e

        for name, e in self.get_elements(node):
            qname = QName(f"{{{namespace}}}{name}")
            self._elements[qname] = e

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

    def get_restriction(self, node: _EtreeElement) -> List[_EtreeElement]:
        return list(node.iterchildren(self.xsd_restriction))

    def get_enumeration(self, node: _EtreeElement) -> List[_EtreeElement]:
        result = list()
        for restriction in self.get_restriction(node):
            result += list(restriction.iterchildren(self.xsd_enumeration))
        return result

    def get_enumeration_values(self, node: _EtreeElement) -> List[str]:
        enumerations = self.get_enumeration(node)
        return list(e.get("value") for e in enumerations)
