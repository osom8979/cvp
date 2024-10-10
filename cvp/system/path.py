# -*- coding: utf-8 -*-

from os import PathLike
from pathlib import Path
from typing import Union


class PathFlavour(Path):
    # noinspection PyProtectedMember
    _flavour = Path()._flavour  # type: ignore[attr-defined]

    def __init__(self, *_):
        super().__init__()

    def as_path(self):
        return Path(self)

    @classmethod
    def classname_subdir(cls, parent: Union[str, PathLike[str]]):
        return cls(Path(parent) / cls.__name__.lower())
