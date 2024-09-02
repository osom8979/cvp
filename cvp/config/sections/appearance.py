# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config._base import BaseConfig
from cvp.config.sections._base import BaseSection


@unique
class _Keys(StrEnum):
    theme = auto()


class AppearanceSection(BaseSection):
    K = _Keys

    def __init__(self, config: BaseConfig, section="appearance"):
        super().__init__(config=config, section=section)

    @property
    def theme(self) -> str:
        return self.get(self.K.theme, "Dark")

    @theme.setter
    def theme(self, value: str) -> None:
        self.set(self.K.theme, value)
