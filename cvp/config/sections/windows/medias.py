# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config._base import BaseConfig
from cvp.config.sections.windows._base import BaseWindowSection
from cvp.variables import MIN_SIDEBAR_WIDTH


@unique
class _Keys(StrEnum):
    sidebar_width = auto()
    selected = auto()


class MediasSection(BaseWindowSection):
    K = _Keys

    def __init__(self, config: BaseConfig, section="medias"):
        super().__init__(config=config, section=section)

    @property
    def sidebar_width(self) -> int:
        return self.get(self.K.sidebar_width, MIN_SIDEBAR_WIDTH)

    @sidebar_width.setter
    def sidebar_width(self, value: int) -> None:
        self.set(self.K.sidebar_width, value)

    @property
    def selected(self) -> str:
        return self.get(self.K.selected, str())

    @selected.setter
    def selected(self, value: str) -> None:
        self.set(self.K.selected, value)