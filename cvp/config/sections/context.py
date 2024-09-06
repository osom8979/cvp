# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config._base import BaseConfig
from cvp.config.sections._base import BaseSection


@unique
class _Keys(StrEnum):
    auto_fixer = auto()


class ContextSection(BaseSection):
    K = _Keys

    def __init__(self, config: BaseConfig, section="context"):
        super().__init__(config=config, section=section)

    @property
    def auto_fixer(self) -> bool:
        return self.get(self.K.auto_fixer, True)

    @auto_fixer.setter
    def auto_fixer(self, value: bool) -> None:
        self.set(self.K.auto_fixer, value)
