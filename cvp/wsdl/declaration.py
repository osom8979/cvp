# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

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
    def wsdl(self):
        if self.document is None:
            transport = Transport(cache=ZeepFileCache(get_wsdl_dir()))
            self.document = Document(
                location=self.location,
                transport=transport,  # noqa
                base=None,
                settings=Settings(),
            )

        assert self.document is not None
        return self.document
