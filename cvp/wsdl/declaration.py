# -*- coding: utf-8 -*-

from typing import NamedTuple


class WsdlDeclaration(NamedTuple):
    namespace: str
    wsdl: str
    binding: str
    """<wsdl:binding name="???" ...>...</wsdl:binding>"""

    @property
    def namespace_binding(self) -> str:
        return "{" + self.namespace + "}" + self.binding
