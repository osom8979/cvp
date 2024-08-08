# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config._base import BaseConfig
from cvp.config.sections._base import BaseSection


@unique
class _Keys(StrEnum):
    opened = auto()


class DemoSection(BaseSection):
    K = _Keys

    def __init__(self, config: BaseConfig, section="demo"):
        super().__init__(config=config, section=section)

    @property
    def opened(self) -> bool:
        return self.get(self.K.opened, False)

    @opened.setter
    def opened(self, value: bool) -> None:
        self.set(self.K.opened, value)
