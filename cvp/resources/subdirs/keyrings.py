# -*- coding: utf-8 -*-

from os import PathLike
from pathlib import Path
from typing import Union

from cvp.keyring.keyring import (
    KeyringBackend,
    get_all_keyring,
    get_keyring_name,
    is_file_backed,
    set_file_path,
)
from cvp.system.path import PathFlavour


class Keyrings(PathFlavour):
    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path)

    def keyring_filepath(self, backend: KeyringBackend, extension=".cfg"):
        filename = get_keyring_name(backend) + extension
        return Path(self / filename)

    def update_default_filepath(self) -> None:
        for backend in get_all_keyring():
            if is_file_backed(backend):
                set_file_path(backend, str(self.keyring_filepath(backend)))
