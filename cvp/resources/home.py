# -*- coding: utf-8 -*-

import os
from os import PathLike
from pathlib import Path
from typing import Optional, Union

from cvp.resources.subdirs.logs import LogsDir
from cvp.resources.subdirs.processes import ProcessesDir
from cvp.system.path import PathFlavour
from cvp.variables import (
    CVP_INI_FILENAME,
    DEFAULT_CVP_HOME_PATH,
    IMGUI_INI_FILENAME,
    LOGGING_JSON_FILENAME,
)


class HomeDir(PathFlavour):
    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path)

        self.logs = LogsDir(Path(self) / "logs")
        self.processes = ProcessesDir(Path(self) / "processes")

        if os.access(self, os.W_OK):
            if not self.is_dir():
                self.mkdir(parents=True, exist_ok=True)
            if not self.logs.is_dir():
                self.logs.mkdir(parents=False, exist_ok=True)
            if not self.processes.is_dir():
                self.processes.mkdir(parents=False, exist_ok=True)

        self.cvp_ini = Path(self) / CVP_INI_FILENAME
        self.imgui_ini = Path(self) / IMGUI_INI_FILENAME
        self.logging_json = Path(self) / LOGGING_JSON_FILENAME

    @classmethod
    def from_path(cls, path: Optional[Union[str, PathLike[str]]] = None):
        return cls(path if path else DEFAULT_CVP_HOME_PATH)
