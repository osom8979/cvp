# -*- coding: utf-8 -*-

import os
from os import PathLike
from typing import Optional, Union

from cvp.resources.subdirs.bin import Bin
from cvp.resources.subdirs.cache import Cache
from cvp.resources.subdirs.keyrings import Keyrings
from cvp.resources.subdirs.layouts import Layouts
from cvp.resources.subdirs.logs import Logs
from cvp.resources.subdirs.processes import Processes
from cvp.resources.subdirs.temp import Temp
from cvp.system.path import PathFlavour
from cvp.variables import (
    CVP_HOME_DIRNAME,
    CVP_YML_FILENAME,
    GUI_INI_FILENAME,
    LOGGING_JSON_FILENAME,
)


class HomeDir(PathFlavour):
    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path)

        self.bin = Bin.classname_subdir(self)
        self.cache = Cache.classname_subdir(self)
        self.keyrings = Keyrings.classname_subdir(self)
        self.layouts = Layouts.classname_subdir(self)
        self.logs = Logs.classname_subdir(self)
        self.processes = Processes.classname_subdir(self)
        self.temp = Temp.classname_subdir(self)

        self._dirs = [
            self.bin,
            self.cache,
            self.keyrings,
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

        self.cvp_yml = self.as_path() / CVP_YML_FILENAME
        self.gui_ini = self.as_path() / GUI_INI_FILENAME
        self.logging_json = self.as_path() / LOGGING_JSON_FILENAME

        self.keyrings.update_default_filepath()

    @classmethod
    def from_path(cls, path: Optional[Union[str, PathLike[str]]] = None):
        return cls(path if path else cls.default_home_path())

    @classmethod
    def default_home_path(cls):
        return str(cls.home() / CVP_HOME_DIRNAME)
