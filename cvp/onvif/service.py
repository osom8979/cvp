# -*- coding: utf-8 -*-

from typing import Dict, Final

from cvp.onvif.types import GetServicesResponse, Service
from cvp.resources.home import HomeDir

DeviceBinding: Final[str] = "DeviceBinding"
GetServices: Final[str] = "GetServices"


class OnvifServiceMapper(Dict[str, Service]):
    def __init__(
        self,
        home: HomeDir,
        uuid: str,
        binding=DeviceBinding,
        api=GetServices,
    ):
        super().__init__()
        self._home = home
        self.uuid = uuid
        self.binding = binding
        self.api = api

    def has_cache(self) -> bool:
        return self._home.onvifs.has_onvif_object(self.uuid, self.binding, self.api)

    def read_cache(self) -> GetServicesResponse:
        return self._home.onvifs.read_onvif_object(self.uuid, self.binding, self.api)

    def update_with_cache(self) -> None:
        if not self.has_cache():
            return
        self.update_with_response(self.read_cache())

    def update_with_response(self, response: GetServicesResponse):
        for service in response:
            self.__setattr__(service.Namespace, service)
