# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from lxml.etree import QName
from zeep.settings import Settings
from zeep.transports import Transport
from zeep.wsdl import Document

from cvp.assets import get_wsdl_dir
from cvp.wsdl.cache import ZeepFileCache


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
        transport = Transport(cache=ZeepFileCache(get_wsdl_dir()))
        return Document(
            location=self.location,
            transport=transport,  # noqa
            base=None,
            settings=Settings(),
        )

    def load_document(self) -> None:
        self.document = self.create_document()

    @property
    def wsdl(self):
        if self.document is None:
            self.load_document()
        assert self.document is not None
        return self.document
