# -*- coding: utf-8 -*-

from typing import Dict, Optional, Tuple

from zeep import Client
from zeep.proxy import OperationProxy, ServiceProxy
from zeep.wsdl.definitions import Binding
from zeep.wsse import UsernameToken

from cvp.wsdl.declaration import WsdlDeclaration


def create_username_token(
    username: Optional[str],
    password: Optional[str],
    use_digest=False,
) -> Optional[UsernameToken]:
    if not username:
        return None
    if not password:
        return None
    return UsernameToken(username=username, password=password, use_digest=use_digest)


def create_client_and_service(
    decl: WsdlDeclaration,
    address: str,
    no_verify=False,
    no_cache=False,
    cache_dir: Optional[str] = None,
    with_http_basic=False,
    with_http_digest=False,
    username: Optional[str] = None,
    password: Optional[str] = None,
    use_digest=False,
) -> Tuple[Client, ServiceProxy]:
    if not address:
        raise ValueError("The 'address' argument is required.")

    client = decl.create_client(
        wsse=create_username_token(username, password, use_digest),
        cache_dir=None if no_cache else cache_dir,
        with_http_basic=with_http_basic,
        with_http_digest=with_http_digest,
        verify=not no_verify,
    )
    service = client.create_service(decl.namespace_binding, address)
    return client, service


class WsdlService:
    __wsdl_declaration__: WsdlDeclaration

    def __init__(
        self,
        address: str,
        no_verify=False,
        no_cache=False,
        cache_dir: Optional[str] = None,
        with_http_basic=False,
        with_http_digest=False,
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_digest=False,
        decl: Optional[WsdlDeclaration] = None,
    ):
        self._address = address
        self._decl = decl if decl is not None else self.__wsdl_declaration__
        assert self._decl is not None
        assert isinstance(self._decl, WsdlDeclaration)

        client, service = create_client_and_service(
            decl=self._decl,
            address=address,
            no_verify=no_verify,
            no_cache=no_cache,
            cache_dir=cache_dir,
            with_http_basic=with_http_basic,
            with_http_digest=with_http_digest,
            username=username,
            password=password,
            use_digest=use_digest,
        )

        self._client = client
        self._service = service

    @property
    def address(self):
        return self._address

    @property
    def declaration(self):
        return self._decl

    @property
    def namespace(self):
        return self._decl.namespace

    @property
    def binding_name(self):
        return self._decl.binding

    @property
    def client(self):
        return self._client

    @property
    def service(self):
        return self._service

    def __repr__(self):
        return (
            f"<{type(self).__name__} @{id(self)}"
            f" namespace='{self.namespace}'"
            f" binding='{self.binding_name}'"
            f" address='{self.address}'"
            ">"
        )

    @property
    def binding(self) -> Binding:
        # noinspection PyProtectedMember
        return self._service._binding

    @property
    def operations(self) -> Dict[str, OperationProxy]:
        # noinspection PyProtectedMember
        return self.binding._operations
