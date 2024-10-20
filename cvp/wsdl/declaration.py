# -*- coding: utf-8 -*-

from typing import Optional

from requests import Session
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from zeep import Client, Transport
from zeep.wsse import UsernameToken

from cvp.logging.logging import wsdl_logger as logger
from cvp.wsdl.cache import ZeepFileCache


class WsdlDeclaration:
    def __init__(
        self,
        namespace: str,
        wsdl: str,
        binding: str,
    ):
        self.namespace = namespace
        self.wsdl = wsdl
        self.binding = binding  # <wsdl:binding name="???" ...> ... </wsdl:binding>

    def create_client(
        self,
        wsse: Optional[UsernameToken] = None,
        cache_dir: Optional[str] = None,
        with_http_basic=False,
        with_http_digest=False,
        verify=True,
    ):
        cache = ZeepFileCache(cache_dir) if cache_dir else None
        session = Session()
        session.verify = verify

        if wsse:
            if with_http_basic and with_http_digest:
                raise ValueError(
                    "The 'with_http_basic' and 'with_http_digest' flags cannot coexist"
                )
            if with_http_basic:
                assert not with_http_digest
                session.auth = HTTPBasicAuth(wsse.username, wsse.password)
            if with_http_digest:
                assert not with_http_basic
                if not wsse.use_digest:
                    logger.warning("<UsernameToken> should be encoded as a digest.")
                session.auth = HTTPDigestAuth(wsse.username, wsse.password)

        transport = Transport(cache=cache, session=session)
        return Client(wsdl=self.wsdl, wsse=wsse, transport=transport)

    @property
    def namespace_binding(self) -> str:
        return "{" + self.namespace + "}" + self.binding
