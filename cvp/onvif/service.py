# -*- coding: utf-8 -*-

from typing import Any, Dict, Final, Iterator, Optional, Protocol, Tuple
from urllib.parse import urlparse, urlunparse

from cvp.resources.subdirs.pickles import Pickles

DeviceBinding: Final[str] = "DeviceBinding"
GetServices: Final[str] = "GetServices"


class OnvifVersion(Protocol):
    Major: int
    Minor: int


class Service(Protocol):
    Namespace: str
    XAddr: str
    Capabilities: Optional[Any]
    Version: OnvifVersion


class GetServicesResponse(Protocol):
    def __iter__(self) -> Iterator[Service]: ...
    def __getitem__(self, index: int) -> Service: ...
    def __len__(self) -> int: ...


class OnvifServiceMapper(Dict[str, Service]):
    def __init__(
        self,
        uuid: str,
        same_host: bool,
        address: str,
        pickles: Pickles,
        *,
        binding_name=DeviceBinding,
        operation_name=GetServices,
    ):
        super().__init__()
        self._uuid = uuid
        self._same_host = same_host
        self._address = address
        self._pickles = pickles
        self._binding_name = binding_name
        self._operation_name = operation_name

    @property
    def cache_args(self) -> Tuple[str, str, str]:
        return self._uuid, self._binding_name, self._operation_name

    def has_cache(self) -> bool:
        return self._pickles.has_object(*self.cache_args)

    def read_cache(self) -> GetServicesResponse:
        return self._pickles.read_object(*self.cache_args)

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

        if not self._same_host:
            return service.XAddr

        src_url = urlparse(self._address)
        new_url = urlparse(service.XAddr)
        new_url._replace(netloc=src_url.netloc)
        return str(urlunparse(new_url))
