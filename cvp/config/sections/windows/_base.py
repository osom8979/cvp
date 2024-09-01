# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config._base import BaseConfig
from cvp.config.sections._base import BaseSection


@unique
class BaseWindowKeys(StrEnum):
    opened = auto()


class BaseWindowSection(BaseSection):
    BWK = BaseWindowKeys

    def __init__(self, config: BaseConfig, section: str):
        super().__init__(config=config, section=section)

    @property
    def opened(self) -> bool:
        return self.get(self.BWK.opened, False)

    @opened.setter
    def opened(self, value: bool) -> None:
        self.set(self.BWK.opened, value)
