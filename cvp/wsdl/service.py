# -*- coding: utf-8 -*-

from typing import Optional, Tuple

from zeep import Client
from zeep.proxy import ServiceProxy
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
    binding_name = decl.get_service_binding_name()
    service = client.create_service(binding_name, address)
    return client, service
