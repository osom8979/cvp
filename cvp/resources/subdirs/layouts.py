# -*- coding: utf-8 -*-

from os import PathLike, remove
from typing import Union

import imgui
from cvp.system.path import PathFlavour


class LayoutsDir(PathFlavour):
    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path)

    def key_filename(self, key: str) -> str:
        return str(self / f"{key}.ini")

    def has_layout(self, key: str) -> bool:
        return (self / self.key_filename(key)).exists()

    def save_layout(self, key: str) -> None:
        imgui.save_ini_settings_to_disk(self.key_filename(key))

    def load_layout(self, key: str) -> None:
        imgui.load_ini_settings_from_disk(self.key_filename(key))

    def remove_layout(self, key: str) -> None:
        remove(str(self / self.key_filename(key)))
