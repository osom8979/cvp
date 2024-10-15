# -*- coding: utf-8 -*-

from typing import Optional, Type, TypeVar

from cvp.config.sections.onvif import OnvifConfig
from cvp.config.sections.onvif import OnvifService as OnvifServiceConfig
from cvp.config.sections.wsdl import WsdlConfig
from cvp.onvif.service.analytics import OnvifAnalytics
from cvp.onvif.service.deviceio import OnvifDeviceIO
from cvp.onvif.service.devicemgmt import OnvifDeviceManagement
from cvp.onvif.service.events import OnvifEvents
from cvp.onvif.service.imaging import OnvifImaging
from cvp.onvif.service.media import OnvifMedia
from cvp.onvif.service.ptz import OnvifPTZ
from cvp.resources.home import HomeDir
from cvp.wsdl.service import WsdlService

WsdlServiceT = TypeVar("WsdlServiceT", bound=WsdlService)


def find_onvif_service_config(
    onvif_config: OnvifConfig,
    wsdl_service_cls: Type[WsdlService],
) -> Optional[OnvifServiceConfig]:
    index = onvif_config.find_service(wsdl_service_cls.__wsdl_declaration__.declaration)
    if 0 <= index < len(onvif_config.services):
        return onvif_config.services[index]
    else:
        return None


def make_wsdl_service_args(
    address: str,
    onvif_config: OnvifConfig,
    wsdl_config: WsdlConfig,
    home: HomeDir,
):
    return dict(
        address=address,
        no_verify=onvif_config.no_verify,
        no_cache=wsdl_config.no_cache,
        cache_dir=str(home.wsdl),
        with_http_basic=onvif_config.is_http_basic,
        with_http_digest=onvif_config.is_http_digest,
        username=onvif_config.username,
        password=home.keyrings.get_onvif_password(onvif_config.uuid),
        use_digest=onvif_config.encode_digest,
        decl=None,
    )


class OnvifService:
    def __init__(
        self,
        onvif_config: OnvifConfig,
        wsdl_config: WsdlConfig,
        home: HomeDir,
    ):
        self._onvif_config = onvif_config
        self._wsdl_config = wsdl_config
        self._home = home

        def _create_onvif_service(cls: Type[WsdlServiceT]) -> Optional[WsdlServiceT]:
            service = find_onvif_service_config(onvif_config, cls)
            if service is None:
                return None
            address = service.xaddr
            args = make_wsdl_service_args(address, onvif_config, wsdl_config, home)
            return cls(**args)

        self._analytics = _create_onvif_service(OnvifAnalytics)
        self._device_io = _create_onvif_service(OnvifDeviceIO)
        self._device_management = _create_onvif_service(OnvifDeviceManagement)
        self._events = _create_onvif_service(OnvifEvents)
        self._imaging = _create_onvif_service(OnvifImaging)
        self._media = _create_onvif_service(OnvifMedia)
        self._ptz = _create_onvif_service(OnvifPTZ)

    @property
    def analytics(self):
        return self._analytics

    @property
    def device_io(self):
        return self._device_io

    @property
    def device_management(self):
        return self._device_management

    @property
    def events(self):
        return self._events

    @property
    def imaging(self):
        return self._imaging

    @property
    def media(self):
        return self._media

    @property
    def ptz(self):
        return self._ptz
