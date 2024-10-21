# -*- coding: utf-8 -*-

from typing import Dict, Final, Optional

from zeep import Client, Transport
from zeep.proxy import OperationProxy, ServiceProxy
from zeep.wsse import UsernameToken

from cvp.wsdl.declaration import WsdlDeclaration

ADDRESS_OPTION_KEY: Final[str] = "address"


class WsdlClient:
    def __init__(
        self,
        declaration: WsdlDeclaration,
        wsse: Optional[UsernameToken] = None,
        transport: Optional[Transport] = None,
        address: Optional[str] = None,
    ):
        self._declaration = declaration
        self._client = Client(wsdl=declaration.wsdl, wsse=wsse, transport=transport)
        self._binding = self._client.wsdl.bindings[self.declaration.namespace_binding]
        binding_options = {ADDRESS_OPTION_KEY: address}
        self._service = ServiceProxy(self._client, self._binding, **binding_options)

    @property
    def declaration(self):
        return self._declaration

    @property
    def namespace(self):
        return self._declaration.namespace

    @property
    def namespace_binding(self):
        return self._declaration.namespace_binding

    @property
    def binding_name(self):
        return self._declaration.binding

    @property
    def client(self):
        return self._client

    @property
    def binding(self):
        return self._binding

    @property
    def service(self):
        return self._service

    @property
    def operations(self) -> Dict[str, OperationProxy]:
        # noinspection PyProtectedMember
        return self._service._operations

    @property
    def binding_options(self):
        # noinspection PyProtectedMember
        return self._service._binding_options

    @property
    def address(self) -> Optional[str]:
        return self.binding_options[ADDRESS_OPTION_KEY]

    @address.setter
    def address(self, value: str) -> None:
        self.binding_options[ADDRESS_OPTION_KEY] = value

    @property
    def has_address(self) -> bool:
        return ADDRESS_OPTION_KEY in self.binding_options

    def __repr__(self):
        return (
            f"<{type(self).__name__} @{id(self)}"
            f" {self.declaration.namespace_binding}"
            ">"
        )

    def __getattr__(self, key):
        return self._service[key]

    def __getitem__(self, key):
        return self._service[key]

    def __iter__(self):
        return self._service.__iter__()
