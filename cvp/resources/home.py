# -*- coding: utf-8 -*-

import os
from os import PathLike
from typing import Optional, Union

from cvp.resources.subdirs.bin import BinDir
from cvp.resources.subdirs.cache import CacheDir
from cvp.resources.subdirs.layouts import LayoutsDir
from cvp.resources.subdirs.logs import LogsDir
from cvp.resources.subdirs.processes import ProcessesDir
from cvp.resources.subdirs.temp import TempDir
from cvp.system.path import PathFlavour
from cvp.variables import (
    CVP_INI_FILENAME,
    DEFAULT_CVP_HOME_PATH,
    GUI_INI_FILENAME,
    LOGGING_JSON_FILENAME,
)


class HomeDir(PathFlavour):
    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path)

        self.bin = BinDir(self.as_path() / "bin")
        self.cache = CacheDir(self.as_path() / "cache")
        self.layouts = LayoutsDir(self.as_path() / "layouts")
        self.logs = LogsDir(self.as_path() / "logs")
        self.processes = ProcessesDir(self.as_path() / "processes")
        self.temp = TempDir(self.as_path() / "temp")

        self._dirs = [
            self.bin,
            self.cache,
            self.layouts,
            self.logs,
            self.processes,
            self.temp,
        ]

        if os.access(self, os.W_OK):
            if not self.is_dir():
                self.mkdir(parents=True, exist_ok=True)
            for dir_path in self._dirs:
                if not dir_path.is_dir():
                    dir_path.mkdir(parents=False, exist_ok=True)

        self.cvp_ini = self.as_path() / CVP_INI_FILENAME
        self.gui_ini = self.as_path() / GUI_INI_FILENAME
        self.logging_json = self.as_path() / LOGGING_JSON_FILENAME

    @classmethod
    def from_path(cls, path: Optional[Union[str, PathLike[str]]] = None):
        return cls(path if path else DEFAULT_CVP_HOME_PATH)
