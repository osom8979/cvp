# -*- coding: utf-8 -*-

from typing import Dict, Final, Optional, Tuple
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
        binding_name=DeviceBinding,
        operation_name=GetServices,
    ):
        super().__init__()
        self._onvif_config = onvif_config
        self._home = home
        self._binding_name = binding_name
        self._operation_name = operation_name

    @property
    def cache_args(self) -> Tuple[str, str, str]:
        return self._onvif_config.uuid, self._binding_name, self._operation_name

    def has_cache(self) -> bool:
        return self._home.pickles.has_object(*self.cache_args)

    def read_cache(self) -> GetServicesResponse:
        return self._home.pickles.read_object(*self.cache_args)

    def update_with_cache(self) -> None:
        if not self.has_cache():
            return
        self.update_with_response(self.read_cache())

    def update_with_response(self, response: GetServicesResponse) -> None:
        for service in response:
            self.__setitem__(service.Namespace, service)

    def get_address(self, namespace: str) -> Optional[str]:
        service = self.get(namespace)
        if service is None:
            return None

        if not self._onvif_config.same_host:
            return service.XAddr

        src_url = urlparse(self._onvif_config.address)
        new_url = urlparse(service.XAddr)
        return str(urlunparse(new_url._replace(netloc=src_url.netloc)))
