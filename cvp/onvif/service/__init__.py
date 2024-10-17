# -*- coding: utf-8 -*-

from typing import Dict, Optional, Type, TypeVar

from cvp.config.sections.onvif import OnvifConfig
from cvp.config.sections.wsdl import WsdlConfig
from cvp.onvif.service.analytics import OnvifAnalytics
from cvp.onvif.service.deviceio import OnvifDeviceIO
from cvp.onvif.service.devicemgmt import OnvifDeviceManagement
from cvp.onvif.service.events import OnvifEvents
from cvp.onvif.service.imaging import OnvifImaging
from cvp.onvif.service.media import OnvifMedia
from cvp.onvif.service.ptz import OnvifPTZ
from cvp.onvif.types import Service
from cvp.resources.home import HomeDir
from cvp.wsdl.service import WsdlService

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

        self._analytics = None
        self._device_io = None
        self._device_management = None
        self._events = None
        self._imaging = None
        self._media = None
        self._ptz = None

        self._services = dict()

    def create_service(self, cls: Type[WsdlServiceT]) -> Optional[WsdlServiceT]:
        namespace = cls.__wsdl_declaration__.declaration
        service = self._services.get(namespace)
        if service is None:
            return None

        return cls(
            address=service.XAddr,
            no_verify=self._onvif_config.no_verify,
            no_cache=self._wsdl_config.no_cache,
            cache_dir=str(self._home.wsdl),
            with_http_basic=self._onvif_config.is_http_basic,
            with_http_digest=self._onvif_config.is_http_digest,
            username=self._onvif_config.username,
            password=self._home.keyrings.get_onvif_password(self._onvif_config.uuid),
            use_digest=self._onvif_config.encode_digest,
            decl=None,
        )

    def update_services(self):
        response = self.device_management.get_services(include_capability=False)
        self._services = {service.Namespace: service for service in response}
        return self._services

    @property
    def services(self):
        return self._services

    @property
    def analytics(self):
        if self._analytics is None:
            self._analytics = self.create_service(OnvifAnalytics)
        return self._analytics

    @property
    def device_io(self):
        if self._device_io is None:
            self._device_io = self.create_service(OnvifDeviceIO)
        return self._device_io

    @property
    def device_management(self):
        if self._device_management is None:
            self._device_management = self.create_service(OnvifDeviceManagement)
        return self._device_management

    @property
    def events(self):
        if self._events is None:
            self._events = self.create_service(OnvifEvents)
        return self._events

    @property
    def imaging(self):
        if self._imaging is None:
            self._imaging = self.create_service(OnvifImaging)
        return self._imaging

    @property
    def media(self):
        if self._media is None:
            self._media = self.create_service(OnvifMedia)
        return self._media

    @property
    def ptz(self):
        if self._ptz is None:
            self._ptz = self.create_service(OnvifPTZ)
        return self._ptz
