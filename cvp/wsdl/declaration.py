# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from lxml.etree import QName
from zeep.settings import Settings
from zeep.wsdl import Document

from cvp.wsdl.schema import XsdSchema
from cvp.wsdl.transport import create_transport_with_package_asset


@dataclass
class WsdlDeclaration:
    namespace: str
    location: str
    binding: str
    """<wsdl:binding name="???" ...>...</wsdl:binding>"""

    _document: Optional[Document] = None
    _schema: Optional[XsdSchema] = None

    @property
    def namespace_binding(self) -> str:
        return "{" + self.namespace + "}" + self.binding

    @property
    def qname(self) -> QName:
        return QName(self.namespace_binding)

    def create_document(self):
        return Document(
            location=self.location,
            transport=create_transport_with_package_asset(),  # noqa
            base=None,
            settings=Settings(raw_response=False, xml_huge_tree=True),
        )

    def load_document(self) -> None:
        self._document = self.create_document()

    @property
    def wsdl(self):
        if self._document is None:
            self.load_document()
        assert self._document is not None
        return self._document

    def create_schema(self):
        return XsdSchema.from_target_namespace(
            location=self.location,
            transport=create_transport_with_package_asset(),
            target_namespace=self.namespace,
        )

    def load_schema(self) -> None:
        self._schema = self.create_schema()

    @property
    def schema(self):
        if self._schema is None:
            self.load_schema()
        assert self._schema is not None
        return self._schema
