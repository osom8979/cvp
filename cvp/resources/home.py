# -*- coding: utf-8 -*-

from os import PathLike
from pathlib import Path
from typing import Final, Optional, Union

from cvp.system.path import PathFlavour

DEFAULT_CVP_DIR_NAME: Final[str] = ".cvp"
DEFAULT_CVP_HOME_PATH: Final[str] = str(Path.home() / DEFAULT_CVP_DIR_NAME)


class HomeDir(PathFlavour):
    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path)

    @classmethod
    def from_path(cls, path: Optional[Union[str, PathLike[str]]] = None):
        return cls(path if path else DEFAULT_CVP_HOME_PATH)
