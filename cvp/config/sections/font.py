# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config._base import BaseConfig
from cvp.config.sections._base import BaseSection


@unique
class _Keys(StrEnum):
    family = auto()
    scale = auto()
    pixels = auto()


class FontSection(BaseSection):
    K = _Keys

    def __init__(self, config: BaseConfig, section="font"):
        super().__init__(config=config, section=section)

    @property
    def family(self) -> str:
        return self.get(self.K.family, str())

    @family.setter
    def family(self, value: str) -> None:
        self.set(self.K.family, value)

    @property
    def scale(self) -> float:
        return self.get(self.K.scale, 1.0)

    @scale.setter
    def scale(self, value: float) -> None:
        self.set(self.K.scale, value)

    @property
    def pixels(self) -> int:
        return self.get(self.K.pixels, 14)

    @pixels.setter
    def pixels(self, value: int) -> None:
        self.set(self.K.pixels, value)
