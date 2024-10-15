# -*- coding: utf-8 -*-

from typing import Optional

from cvp.config.sections.onvif import OnvifConfig
from cvp.config.sections.wsdl import WsdlConfig
from cvp.resources.home import HomeDir
from cvp.wsdl.declaration import WsdlDeclaration
from cvp.wsdl.service import create_client_and_service


class OnvifService:
    def __init__(
        self,
        decl: WsdlDeclaration,
        onvif_config: OnvifConfig,
        wsdl_config: WsdlConfig,
        home: HomeDir,
        password: Optional[str] = None,
    ):
        if onvif_config.use_wsse:
            username = onvif_config.username
        else:
            username = None
            password = None

        client, service = create_client_and_service(
            decl=decl,
            address=onvif_config.address,
            no_verify=onvif_config.no_verify,
            no_cache=wsdl_config.no_cache,
            cache_dir=str(home.wsdl),
            with_http_basic=onvif_config.is_http_basic,
            with_http_digest=onvif_config.is_http_digest,
            username=username,
            password=password,
            use_digest=onvif_config.encode_digest,
        )

        self._config = onvif_config
        self._client = client
        self._service = service

    @property
    def client(self):
        return self._client

    @property
    def service(self):
        return self._service
