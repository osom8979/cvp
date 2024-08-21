# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config._base import BaseConfig
from cvp.config.sections._base import BaseSection


@unique
class _CommonWindowKeys(StrEnum):
    opened = auto()


class CommonWindowSection(BaseSection):
    CWK = _CommonWindowKeys

    def __init__(self, config: BaseConfig, section: str):
        super().__init__(config=config, section=section)

    @property
    def opened(self) -> bool:
        return self.get(self.CWK.opened, False)

    @opened.setter
    def opened(self, value: bool) -> None:
        self.set(self.CWK.opened, value)
