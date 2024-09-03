# -*- coding: utf-8 -*-

from pathlib import Path


class PathFlavour(Path):
    # noinspection PyProtectedMember
    _flavour = Path()._flavour  # type: ignore[attr-defined]

    def __init__(self, *_):
        super().__init__()

    def as_path(self):
        return Path(self)
