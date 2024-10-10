# -*- coding: utf-8 -*-

from argparse import Namespace
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


def create_username_token_with_namespace(args: Namespace) -> Optional[UsernameToken]:
    assert isinstance(args.username, (type(None), str))
    assert isinstance(args.password, (type(None), str))
    assert isinstance(args.use_digest, bool)
    return create_username_token(args.username, args.password, args.use_digest)


def create_client_and_service(
    decl: WsdlDeclaration,
    args: Namespace,
) -> Tuple[Client, ServiceProxy]:
    if not args.address:
        raise ValueError("The 'address' argument is required.")

    assert isinstance(args.no_verify, bool)
    assert isinstance(args.no_cache, bool)
    assert isinstance(args.cache_dir, str)
    assert isinstance(args.with_http_basic, bool)
    assert isinstance(args.with_http_digest, bool)

    client = decl.create_client(
        wsse=create_username_token_with_namespace(args),
        cache_dir=None if args.no_cache else args.cache_dir,
        with_http_basic=args.with_http_basic,
        with_http_digest=args.with_http_digest,
        verify=not args.no_verify,
    )
    binding_name = decl.get_service_binding_name()
    service = client.create_service(binding_name, args.address)
    return client, service


def create_service(decl: WsdlDeclaration, args: Namespace) -> ServiceProxy:
    return create_client_and_service(decl, args)[1]
