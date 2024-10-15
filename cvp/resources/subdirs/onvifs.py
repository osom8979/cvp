# -*- coding: utf-8 -*-

from os import PathLike
from pathlib import Path
from typing import Union

from cvp.system.path import PathFlavour


class Onvifs(PathFlavour):
    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path)

    def onvif_dirpath(self, uuid: str, subclass: str, api: str):
        return Path(self / uuid / subclass / f"{api}.json")
