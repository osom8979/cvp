# -*- coding: utf-8 -*-

from os import PathLike
from shutil import copytree
from typing import Union

from cvp.assets import get_wsdl_path
from cvp.system.path import PathFlavour


class Wsdl(PathFlavour):
    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path)

    def copy_asset_files(self):
        return copytree(get_wsdl_path(), self, dirs_exist_ok=True)
