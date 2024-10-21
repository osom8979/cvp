# -*- coding: utf-8 -*-

from typing import Dict, Final
from urllib.parse import urlparse, urlunparse

from cvp.config.sections.onvif import OnvifConfig
from cvp.onvif.types import GetServicesResponse, Service
from cvp.resources.home import HomeDir

DeviceBinding: Final[str] = "DeviceBinding"
GetServices: Final[str] = "GetServices"


class OnvifServiceMapper(Dict[str, Service]):
    def __init__(
        self,
        onvif_config: OnvifConfig,
        home: HomeDir,
        *,
        binding=DeviceBinding,
        api=GetServices,
    ):
        super().__init__()
        self._onvif_config = onvif_config
        self._home = home
        self._binding = binding
        self._api = api

    @property
    def uuid(self):
        return self._onvif_config.uuid

    @property
    def binding(self):
        return self._binding

    @property
    def api(self):
        return self._api

    def has_cache(self) -> bool:
        return self._home.onvifs.has_onvif_object(self.uuid, self.binding, self.api)

    def read_cache(self) -> GetServicesResponse:
        return self._home.onvifs.read_onvif_object(self.uuid, self.binding, self.api)

    def update_with_cache(self) -> None:
        if not self.has_cache():
            return
        self.update_with_response(self.read_cache())

    def update_with_response(self, response: GetServicesResponse) -> None:
        for service in response:
            self.__setitem__(service.Namespace, service)

    def get_address(self, namespace: str) -> str:
        service = self.get(namespace)
        if service is None:
            raise KeyError(f"Not found namespace: '{namespace}'")

        if not self._onvif_config.same_host:
            return service.XAddr

        src_url = urlparse(self._onvif_config.address)
        new_url = urlparse(service.XAddr)
        return str(urlunparse(new_url._replace(netloc=src_url.netloc)))
