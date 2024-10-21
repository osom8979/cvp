# -*- coding: utf-8 -*-

from copy import deepcopy
from typing import Any, Optional, ParamSpec, Sequence, TypeVar

from requests import Session
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from zeep import Transport

from cvp.config.sections.onvif import OnvifConfig
from cvp.config.sections.wsdl import WsdlConfig
from cvp.logging.logging import onvif_logger as logger
from cvp.onvif.cached.cache import CachedWsdlClient
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
from cvp.resources.home import HomeDir
from cvp.wsdl.cache import ZeepFileCache
from cvp.wsdl.client import WsdlClient
from cvp.wsdl.wsse import create_username_token

WsdlRequestParam = ParamSpec("WsdlRequestParam")
WsdlResponseT = TypeVar("WsdlResponseT")
WsdlServiceT = TypeVar("WsdlServiceT", bound=WsdlClient)


class OnvifClient:
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

        no_cache = self._wsdl_config.no_cache
        cache_dir = str(home.wsdl)

        self._session = Session()
        self._session.verify = not onvif_config.no_verify
        self._cache = None if no_cache else ZeepFileCache(cache_dir)
        self._wsse = create_username_token(username, password, use_digest)
        self._transport = Transport(cache=self._cache, session=self._session)
        self._services = OnvifServiceMapper(self._onvif_config, self._home)

        if self._wsse is not None:
            assert username is not None
            assert password is not None
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

        self.devicemgmt = self.create_wsdl(ONVIF_DEVICEMGMT, self._onvif_config.address)
        self.analytics = self.create_wsdl(ONVIF_ANALYTICS)
        self.deviceio = self.create_wsdl(ONVIF_DEVICEIO)
        self.events = self.create_wsdl(ONVIF_EVENTS)
        self.imaging = self.create_wsdl(ONVIF_IMAGING)
        self.media = self.create_wsdl(ONVIF_MEDIA)
        self.notification = self.create_wsdl(ONVIF_NOTIFICATION)
        self.ptz = self.create_wsdl(ONVIF_PTZ)
        self.pullpoint = self.create_wsdl(ONVIF_PULLPOINT)
        self.receiver = self.create_wsdl(ONVIF_RECEIVER)
        self.recording = self.create_wsdl(ONVIF_RECODING)
        self.replay = self.create_wsdl(ONVIF_REPLAY)
        self.search = self.create_wsdl(ONVIF_SEARCH)
        self.subscription = self.create_wsdl(ONVIF_SUBSCRIPTION)

    @property
    def wsdls(self) -> Sequence[CachedWsdlClient]:
        return (
            self.devicemgmt,
            self.analytics,
            self.deviceio,
            self.events,
            self.imaging,
            self.media,
            self.notification,
            self.ptz,
            self.pullpoint,
            self.receiver,
            self.recording,
            self.replay,
            self.search,
            self.subscription,
        )

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

    def create_wsdl(
        self,
        declaration: WsdlDeclaration,
        address: Optional[str] = None,
        *,
        update_onvif_ns_prefixes=False
    ):
        result = CachedWsdlClient(
            onvif_config=self._onvif_config,
            home=self._home,
            declaration=declaration,
            wsse=self._wsse,
            transport=self._transport,
            address=address,
        )
        if update_onvif_ns_prefixes:
            result.update_onvif_ns_prefixes()
        return result

    @property
    def onvif_config(self):
        return self._onvif_config

    @property
    def wsdl_config(self):
        return self._wsdl_config

    @property
    def services(self):
        return self._services

    def update_services(self) -> None:
        response = self.devicemgmt.GetServices(IncludeCapability=False)
        self._services.update_with_response(response)
        for wsdl in self.wsdls:
            try:
                wsdl.address = self._services.get_address(wsdl.namespace)
            except KeyError:
                continue
