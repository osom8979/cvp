# -*- coding: utf-8 -*-

from typing import Any, Callable, Dict, Optional, ParamSpec, Type, TypeVar

from cvp.config.sections.onvif import OnvifConfig
from cvp.config.sections.wsdl import WsdlConfig
from cvp.logging.logging import onvif_logger as logger
from cvp.onvif.service.analytics import OnvifAnalytics
from cvp.onvif.service.deviceio import OnvifDeviceIO
from cvp.onvif.service.devicemgmt import OnvifDeviceManagement
from cvp.onvif.service.events import OnvifEvents
from cvp.onvif.service.imaging import OnvifImaging
from cvp.onvif.service.media import OnvifMedia
from cvp.onvif.service.ptz import OnvifPTZ
from cvp.onvif.types import GetServicesResponse, Service
from cvp.resources.home import HomeDir
from cvp.wsdl.service import WsdlService

WsdlRequestParam = ParamSpec("WsdlRequestParam")
WsdlResponseT = TypeVar("WsdlResponseT")
WsdlServiceT = TypeVar("WsdlServiceT", bound=WsdlService)


class OnvifService:
    _analytics: Optional[OnvifAnalytics]
    _device_io: Optional[OnvifDeviceIO]
    _device_management: Optional[OnvifDeviceManagement]
    _events: Optional[OnvifEvents]
    _imaging: Optional[OnvifImaging]
    _media: Optional[OnvifMedia]
    _ptz: Optional[OnvifPTZ]
    _services: Dict[str, Service]

    def __init__(
        self,
        onvif_config: OnvifConfig,
        wsdl_config: WsdlConfig,
        home: HomeDir,
    ):
        self._onvif_config = onvif_config
        self._wsdl_config = wsdl_config
        self._home = home

        self._services = dict()
        self._analytics = None
        self._device_io = None
        self._device_management = None
        self._events = None
        self._imaging = None
        self._media = None
        self._ptz = None

    def clear(self):
        self._services = dict()
        self._analytics = None
        self._device_io = None
        self._device_management = None
        self._events = None
        self._imaging = None
        self._media = None
        self._ptz = None

    def has_cache(self, wsdl: WsdlService, api: str) -> bool:
        uuid = self._onvif_config.uuid
        subclass = wsdl.__wsdl_declaration__.subclass
        return self._home.onvifs.has_onvif_object(uuid, subclass, api)

    def read_cache(self, wsdl: WsdlService, api: str) -> Any:
        uuid = self._onvif_config.uuid
        subclass = wsdl.__wsdl_declaration__.subclass
        return self._home.onvifs.read_onvif_object(uuid, subclass, api)

    def write_cache(self, wsdl: WsdlService, api: str, o: Any):
        uuid = self._onvif_config.uuid
        subclass = wsdl.__wsdl_declaration__.subclass
        return self._home.onvifs.write_onvif_object(uuid, subclass, api, o)

    def call(
        self,
        wsdl: WsdlService,
        func: Callable[WsdlRequestParam, WsdlResponseT],
        *args: WsdlRequestParam.args,
        **kwargs: WsdlRequestParam.kwargs,
    ) -> WsdlResponseT:
        api = func.__name__
        if not hasattr(wsdl, api):
            raise AttributeError(f"API method '{api}' not found in the WSDL service")

        if self.has_cache(wsdl, api):
            return self.read_cache(wsdl, api)
        else:
            response = getattr(wsdl, api)(*args, **kwargs)
            self.write_cache(wsdl, api, response)
            return response

    def get_services(self, include_capability=False) -> GetServicesResponse:
        return self.call(
            self.device_management,
            OnvifDeviceManagement.get_services,
            include_capability,
        )

    def update_services(self) -> None:
        response = self.get_services(include_capability=False)
        self._services = {service.Namespace: service for service in response}

    def _create_wsdl(
        self,
        cls: Type[WsdlServiceT],
        address: Optional[str] = None,
    ) -> Optional[WsdlServiceT]:
        if not address:
            namespace = cls.__wsdl_declaration__.declaration
            if namespace in self._services:
                address = self._services[namespace].XAddr
            else:
                if issubclass(cls, OnvifDeviceManagement):
                    address = self._onvif_config.address
                else:
                    return None

            if not address:
                return None

        no_verify = self._onvif_config.no_verify
        no_cache = self._wsdl_config.no_cache
        cache_dir = str(self._home.wsdl)

        if self._onvif_config.use_wsse:
            with_http_basic = self._onvif_config.is_http_basic
            with_http_digest = self._onvif_config.is_http_digest
            username = self._onvif_config.username
            password = self._home.keyrings.get_onvif_password(self._onvif_config.uuid)
            use_digest = self._onvif_config.encode_digest
        else:
            with_http_basic = False
            with_http_digest = False
            username = None
            password = None
            use_digest = False

        try:
            return cls(
                address=address,
                no_verify=no_verify,
                no_cache=no_cache,
                cache_dir=cache_dir,
                with_http_basic=with_http_basic,
                with_http_digest=with_http_digest,
                username=username,
                password=password,
                use_digest=use_digest,
                decl=None,
            )
        except BaseException as e:
            logger.error(e)
            return None

    @property
    def analytics(self):
        if self._analytics is None:
            self._analytics = self._create_wsdl(OnvifAnalytics)
        return self._analytics

    @property
    def device_io(self):
        if self._device_io is None:
            self._device_io = self._create_wsdl(OnvifDeviceIO)
        return self._device_io

    @property
    def device_management(self):
        if self._device_management is None:
            self._device_management = self._create_wsdl(OnvifDeviceManagement)
        return self._device_management

    @property
    def events(self):
        if self._events is None:
            self._events = self._create_wsdl(OnvifEvents)
        return self._events

    @property
    def imaging(self):
        if self._imaging is None:
            self._imaging = self._create_wsdl(OnvifImaging)
        return self._imaging

    @property
    def media(self):
        if self._media is None:
            self._media = self._create_wsdl(OnvifMedia)
        return self._media

    @property
    def ptz(self):
        if self._ptz is None:
            self._ptz = self._create_wsdl(OnvifPTZ)
        return self._ptz
