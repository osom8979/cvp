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
        client = Client(wsdl=self.wsdl, wsse=wsse, transport=transport)
        client.set_ns_prefix("tds", "http://www.onvif.org/ver10/device/wsdl")
        client.set_ns_prefix("tev", "http://www.onvif.org/ver10/events/wsdl")
        client.set_ns_prefix("timg", "http://www.onvif.org/ver20/imaging/wsdl")
        client.set_ns_prefix("tmd", "http://www.onvif.org/ver10/deviceIO/wsdl")
        client.set_ns_prefix("tptz", "http://www.onvif.org/ver20/ptz/wsdl")
        client.set_ns_prefix("ttr", "http://www.onvif.org/ver10/media/wsdl")
        client.set_ns_prefix("ter", "http://www.onvif.org/ver10/error")
        return client

    @property
    def namespace_binding(self) -> str:
        return "{" + self.namespace + "}" + self.binding
