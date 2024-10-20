# -*- coding: utf-8 -*-

from copy import deepcopy
from typing import Any, Dict, Final, Optional, ParamSpec, TypeVar
from urllib.parse import urlparse, urlunparse

from requests import Session
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from zeep import Client, Transport
from zeep.proxy import OperationProxy, ServiceProxy

from cvp.config.sections.onvif import OnvifConfig
from cvp.config.sections.wsdl import WsdlConfig
from cvp.logging.logging import onvif_logger as logger
from cvp.onvif.declarations import (
    ONVIF_ANALYTICS,
    ONVIF_DEVICEIO,
    ONVIF_DEVICEMGMT,
    ONVIF_EVENTS,
    ONVIF_IMAGING,
    ONVIF_MEDIA,
    ONVIF_NOTIFICATION,
    ONVIF_PTZ,
    ONVIF_PULLPOINT,
    ONVIF_RECEIVER,
    ONVIF_RECODING,
    ONVIF_REPLAY,
    ONVIF_SEARCH,
    ONVIF_SUBSCRIPTION,
    WsdlDeclaration,
)
from cvp.onvif.service import OnvifServiceMapper
from cvp.onvif.types import Service
from cvp.resources.home import HomeDir
from cvp.wsdl.cache import ZeepCacheBase, ZeepFileCache
from cvp.wsdl.client import WsdlClient
from cvp.wsdl.wsse import create_username_token

WsdlRequestParam = ParamSpec("WsdlRequestParam")
WsdlResponseT = TypeVar("WsdlResponseT")
WsdlServiceT = TypeVar("WsdlServiceT", bound=WsdlClient)

DeviceBinding: Final[str] = "DeviceBinding"
GetServices: Final[str] = "GetServices"


#     assert isinstance(service, WsdlService)
#     service.client.set_ns_prefix("tds", "http://www.onvif.org/ver10/device/wsdl")
#     service.client.set_ns_prefix("tev", "http://www.onvif.org/ver10/events/wsdl")
#     service.client.set_ns_prefix("timg", "http://www.onvif.org/ver20/imaging/wsdl")
#     service.client.set_ns_prefix("tmd", "http://www.onvif.org/ver10/deviceIO/wsdl")
#     service.client.set_ns_prefix("tptz", "http://www.onvif.org/ver20/ptz/wsdl")
#     service.client.set_ns_prefix("ttr", "http://www.onvif.org/ver10/media/wsdl")
#     service.client.set_ns_prefix("ter", "http://www.onvif.org/ver10/error")

#     for key in dir(service):
#         attr = getattr(service, key)
#         if not has_onvif_api(attr):
#             continue
#
#         api_name = get_onvif_api(attr)
#         injected_attr = inject_response_cache(
#             attr,
#             home,
#             onvif_config,
#             cls.__wsdl_declaration__,
#             api_name,
#         )
#         setattr(service, key, injected_attr)
#
#     return service


class OnvifClient:
    _services: Dict[str, Service]
    _cache: Optional[ZeepCacheBase]

    def __init__(
        self,
        onvif_config: OnvifConfig,
        wsdl_config: WsdlConfig,
        home: HomeDir,
    ):
        self._onvif_config = deepcopy(onvif_config)
        self._wsdl_config = deepcopy(wsdl_config)
        self._home = home

        if onvif_config.use_wsse:
            with_http_basic = onvif_config.is_http_basic
            with_http_digest = onvif_config.is_http_digest
            username = onvif_config.username
            password = home.keyrings.get_onvif_password(onvif_config.uuid)
            use_digest = onvif_config.encode_digest
        else:
            with_http_basic = False
            with_http_digest = False
            username = None
            password = None
            use_digest = False

        self._session = Session()
        self._session.verify = not onvif_config.no_verify
        self._cache = None if wsdl_config.no_cache else ZeepFileCache(str(home.wsdl))
        self._wsse = create_username_token(username, password, use_digest)
        self._transport = Transport(cache=self._cache, session=self._session)
        self._services = OnvifServiceMapper(self._home, self._onvif_config.uuid)

        if self._wsse is not None:
            if with_http_basic and with_http_digest:
                raise ValueError(
                    "The 'with_http_basic' and 'with_http_digest' flags cannot coexist"
                )
            if with_http_basic:
                assert not with_http_digest
                self._session.auth = HTTPBasicAuth(username, password)
            if with_http_digest:
                assert not with_http_basic
                if not use_digest:
                    logger.warning("<UsernameToken> should be encoded as a digest.")
                self._session.auth = HTTPDigestAuth(username, password)

        self._devicemgmt = self.create_client(ONVIF_DEVICEMGMT, self._onvif_config.address)
        self._analytics = self.create_client(ONVIF_ANALYTICS)
        self._deviceio = self.create_client(ONVIF_DEVICEIO)
        self._events = self.create_client(ONVIF_EVENTS)
        self._imaging = self.create_client(ONVIF_IMAGING)
        self._media = self.create_client(ONVIF_MEDIA)
        self._notification = self.create_client(ONVIF_NOTIFICATION)
        self._ptz = self.create_client(ONVIF_PTZ)
        self._pullpoint = self.create_client(ONVIF_PULLPOINT)
        self._receiver = self.create_client(ONVIF_RECEIVER)
        self._recording = self.create_client(ONVIF_RECODING)
        self._replay = self.create_client(ONVIF_REPLAY)
        self._search = self.create_client(ONVIF_SEARCH)
        self._subscription = self.create_client(ONVIF_SUBSCRIPTION)

    @property
    def uuid(self):
        return self._onvif_config.uuid

    def has_cache(self, binding: str, api: str) -> bool:
        return self._home.onvifs.has_onvif_object(self.uuid, binding, api)

    def read_cache(self, binding: str, api: str) -> Any:
        return self._home.onvifs.read_onvif_object(self.uuid, binding, api)

    def write_cache(self, binding: str, api: str, o: Any) -> int:
        return self._home.onvifs.write_onvif_object(self.uuid, binding, api, o)

    def remove_cache(self, binding: str, api: str) -> None:
        self._home.onvifs.remove_onvif_object(self.uuid, binding, api)

    def create_client(
        self,
        declaration: WsdlDeclaration,
        address: Optional[str] = None,
    ):
        client = WsdlClient(declaration, self._wsse, self._transport, address)
        client.client.set_ns_prefix("tds", "http://www.onvif.org/ver10/device/wsdl")
        client.client.set_ns_prefix("tev", "http://www.onvif.org/ver10/events/wsdl")
        client.client.set_ns_prefix("timg", "http://www.onvif.org/ver20/imaging/wsdl")
        client.client.set_ns_prefix("tmd", "http://www.onvif.org/ver10/deviceIO/wsdl")
        client.client.set_ns_prefix("tptz", "http://www.onvif.org/ver20/ptz/wsdl")
        client.client.set_ns_prefix("ttr", "http://www.onvif.org/ver10/media/wsdl")
        client.client.set_ns_prefix("ter", "http://www.onvif.org/ver10/error")
        return client

    @property
    def onvif_config(self):
        return self._onvif_config

    @property
    def services(self):
        return self._services

    # def create_wsdl(
    #     self,
    #     cls: Type[WsdlServiceT],
    #     services: Optional[Dict[str, Service]] = None,
    # ) -> Optional[WsdlServiceT]:
    #     services = services if services else self._services
    #     assert services is not None
    #
    #     namespace = cls.__wsdl_declaration__.namespace
    #     service = services.get(namespace)
    #     if service is None:
    #         return None
    #
    #     if self._onvif_config.same_host:
    #         src_url = urlparse(self._onvif_config.address)
    #         new_url = urlparse(service.XAddr)
    #         address = str(urlunparse(new_url._replace(netloc=src_url.netloc)))
    #     else:
    #         address = service.XAddr
    #
    #     return _create_wsdl_service(
    #         cls=cls,
    #         onvif_config=self._onvif_config,
    #         wsdl_config=self._wsdl_config,
    #         home=self._home,
    #         address=address,
    #     )
