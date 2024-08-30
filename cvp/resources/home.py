# -*- coding: utf-8 -*-

from os import PathLike
from pathlib import Path
from typing import Final, Optional, Union

DEFAULT_CVP_DIR_NAME: Final[str] = ".cvp"
DEFAULT_CVP_HOME_PATH: Final[str] = str(Path.home() / DEFAULT_CVP_DIR_NAME)


class HomeDir(Path):
    # noinspection PyProtectedMember
    _flavour = Path()._flavour  # type: ignore[attr-defined]

    @classmethod
    def from_path(cls, path: Optional[Union[str, PathLike[str]]] = None):
        return cls(path if path else DEFAULT_CVP_HOME_PATH)
