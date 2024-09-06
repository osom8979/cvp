# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from typing import Tuple

from cvp.config._base import BaseConfig
from cvp.config.sections._base import BaseSection


@unique
class _Keys(StrEnum):
    width = auto()
    height = auto()
    fullscreen = auto()
    force_egl = auto()


class DisplaySection(BaseSection):
    K = _Keys

    def __init__(self, config: BaseConfig, section="display"):
        super().__init__(config=config, section=section)

    @property
    def width(self) -> int:
        return self.get(self.K.width, -1)

    @width.setter
    def width(self, value: int) -> None:
        self.set(self.K.width, value)

    @property
    def height(self) -> int:
        return self.get(self.K.height, -1)

    @height.setter
    def height(self, value: int) -> None:
        self.set(self.K.height, value)

    @property
    def size(self) -> Tuple[int, int]:
        return self.width, self.height

    @size.setter
    def size(self, value: Tuple[int, int]) -> None:
        self.width = value[0]
        self.height = value[1]

    @property
    def fullscreen(self) -> bool:
        return self.get(self.K.fullscreen, False)

    @fullscreen.setter
    def fullscreen(self, value: bool) -> None:
        self.set(self.K.fullscreen, value)
