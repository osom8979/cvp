# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config._base import BaseConfig
from cvp.config.sections.windows._base import BaseWindowSection
from cvp.variables import MIN_SIDEBAR_WIDTH


@unique
class BaseManagerKeys(StrEnum):
    sidebar_width = auto()
    selected = auto()


class BaseManagerSection(BaseWindowSection):
    BMK = BaseManagerKeys

    def __init__(self, config: BaseConfig, section: str):
        super().__init__(config=config, section=section)

    @property
    def has_sidebar_width(self) -> bool:
        return self.has(self.BMK.sidebar_width)

    @property
    def sidebar_width(self) -> int:
        return self.get(self.BMK.sidebar_width, MIN_SIDEBAR_WIDTH)

    @sidebar_width.setter
    def sidebar_width(self, value: int) -> None:
        self.set(self.BMK.sidebar_width, value)

    @property
    def has_selected(self) -> bool:
        return self.has(self.BMK.selected)

    @property
    def selected(self) -> str:
        return self.get(self.BMK.selected, str())

    @selected.setter
    def selected(self, value: str) -> None:
        self.set(self.BMK.selected, value)
