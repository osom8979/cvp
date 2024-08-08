# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config._base import BaseConfig
from cvp.config.sections._window import CommonWindowSection


@unique
class _Keys(StrEnum):
    sidebar_width = auto()
    menu_index = auto()


class PreferenceSection(CommonWindowSection):
    K = _Keys

    def __init__(self, config: BaseConfig, section="preference"):
        super().__init__(config=config, section=section)

    @property
    def sidebar_width(self) -> int:
        return self.get(self.K.sidebar_width, 128)

    @sidebar_width.setter
    def sidebar_width(self, value: int) -> None:
        self.set(self.K.sidebar_width, value)

    @property
    def menu_index(self) -> int:
        return self.get(self.K.menu_index, 0)

    @menu_index.setter
    def menu_index(self, value: int) -> None:
        self.set(self.K.menu_index, value)
