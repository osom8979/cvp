# -*- coding: utf-8 -*-

from typing import List, Optional, Union

from requests import Session
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from zeep import Client, Transport
from zeep.wsse import UsernameToken

from cvp.logging.logging import wsdl_logger as logger
from cvp.wsdl.cache import ZeepFileCache


class WsdlDeclaration:
    def __init__(
        self,
        declaration: str,
        http_sub: str,
        wsdl_file: str,
        subclass: str,
        binding_names: Optional[List[str]] = None,
    ):
        self.declaration = declaration
        self.http_sub = http_sub
        self.wsdl_file = wsdl_file
        self.subclass = subclass

        # <wsdl:binding name="???" ...> ... </wsdl:binding>
        self.binding_names = binding_names if binding_names else list()

    @property
    def wsdl_file_url(self) -> str:
        return self.declaration + "/" + self.wsdl_file

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
        return Client(wsdl=self.wsdl_file_url, wsse=wsse, transport=transport)

    def get_service_binding_name(self, index_or_name: Union[str, int] = 0) -> str:
        if isinstance(index_or_name, int):
            return "{" + self.declaration + "}" + self.binding_names[index_or_name]
        else:
            return "{" + self.declaration + "}" + index_or_name
