# -*- coding: utf-8 -*-

from typing import Dict, Optional

from zeep import Client, Transport
from zeep.proxy import OperationProxy, ServiceProxy
from zeep.wsse import UsernameToken

from cvp.wsdl.declaration import WsdlDeclaration


class WsdlClient:
    def __init__(
        self,
        declaration: WsdlDeclaration,
        wsse: UsernameToken,
        transport: Transport,
        address: Optional[str] = None,
    ):
        self._declaration = declaration
        self._client = Client(wsdl=declaration.wsdl, wsse=wsse, transport=transport)
        self._binding = self._client.wsdl.bindings[self.declaration.namespace_binding]

        address = address if address else str()
        assert isinstance(address, str)
        self._service = ServiceProxy(self._client, self._binding, address=address)

    @property
    def declaration(self):
        return self._declaration

    @property
    def client(self):
        return self._client

    @property
    def binding(self):
        return self._binding

    @property
    def operations(self) -> Dict[str, OperationProxy]:
        # noinspection PyProtectedMember
        return self.binding._operations

    @property
    def service(self):
        return self._service

    @property
    def binding_options(self):
        # noinspection PyProtectedMember
        return self._service._binding_options

    @property
    def address(self) -> str:
        return self.binding_options[self.address.__name__]

    @address.setter
    def address(self, value: str) -> None:
        self.binding_options[self.address.__name__] = value

    def __repr__(self):
        return (
            f"<{type(self).__name__} @{id(self)}"
            f" {self.declaration.namespace_binding}"
            ">"
        )
