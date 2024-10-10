# -*- coding: utf-8 -*-

from os import PathLike
from pathlib import Path
from typing import Dict, Optional, Tuple, Union

from cvp.keyring.keyring import (
    KeyringBackend,
    delete_password,
    get_all_keyring,
    get_keyring_name,
    get_password,
    is_file_backed,
    set_file_path,
    set_password,
)
from cvp.system.path import PathFlavour


class Keyrings(PathFlavour):
    _password_cache: Dict[Tuple[str, str], str]

    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path)
        self._onvif_password_service_name = "onvif_password"
        self._password_cache = dict()

    def keyring_filepath(self, backend: KeyringBackend, extension=".cfg"):
        filename = get_keyring_name(backend) + extension
        return Path(self / filename)

    def update_default_filepath(self) -> None:
        for backend in get_all_keyring():
            if is_file_backed(backend):
                set_file_path(backend, str(self.keyring_filepath(backend)))

    def get_password(self, service: str, key: str, default=None) -> Optional[str]:
        cache_key = service, key
        if cache_key in self._password_cache:
            return self._password_cache[cache_key]

        result = get_password(service, key)
        if result is None:
            return default

        self._password_cache[cache_key] = result
        return result

    def set_password(self, service: str, key: str, value: str) -> None:
        cache_key = service, key
        set_password(service, key, value)
        self._password_cache[cache_key] = value

    def delete_password(self, service: str, key: str) -> None:
        cache_key = service, key
        if cache_key in self._password_cache:
            self._password_cache.pop(cache_key)
        if get_password(service, key) is not None:
            delete_password(service, key)

    def get_onvif_password(self, key: str, default=None) -> Optional[str]:
        return self.get_password(self._onvif_password_service_name, key, default)

    def set_onvif_password(self, key: str, value: str) -> None:
        self.set_password(self._onvif_password_service_name, key, value)

    def delete_onvif_password(self, key: str) -> None:
        self.delete_password(self._onvif_password_service_name, key)
