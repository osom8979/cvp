# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from lxml.etree import QName
from zeep.wsdl import Document

from cvp.wsdl.document import create_document_with_package_asset


@dataclass
class WsdlDeclaration:
    namespace: str
    location: str
    binding: str
    """<wsdl:binding name="???" ...>...</wsdl:binding>"""

    document: Optional[Document] = None
    no_asset: bool = False

    @property
    def namespace_binding(self) -> str:
        return "{" + self.namespace + "}" + self.binding

    @property
    def qname(self) -> QName:
        return QName(self.namespace_binding)

    def create_document(self):
        return create_document_with_package_asset(self.location)

    def load_document(self) -> None:
        self.document = self.create_document()

    @property
    def wsdl(self):
        if self.document is None:
            self.load_document()
        assert self.document is not None
        return self.document
