# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config._base import BaseConfig
from cvp.config.sections.windows._base import BaseWindowSection
from cvp.variables import MIN_SIDEBAR_HEIGHT, MIN_SIDEBAR_WIDTH


@unique
class _Keys(StrEnum):
    split_left = auto()
    split_right = auto()
    split_bottom = auto()


class FlowSection(BaseWindowSection):
    K = _Keys

    def __init__(self, config: BaseConfig, section="flow"):
        super().__init__(config=config, section=section)

    @property
    def split_left(self) -> int:
        return self.get(self.K.split_left, MIN_SIDEBAR_WIDTH)

    @split_left.setter
    def split_left(self, value: int) -> None:
        self.set(self.K.split_left, value)

    @property
    def split_right(self) -> int:
        return self.get(self.K.split_right, MIN_SIDEBAR_WIDTH)

    @split_right.setter
    def split_right(self, value: int) -> None:
        self.set(self.K.split_right, value)

    @property
    def split_bottom(self) -> int:
        return self.get(self.K.split_bottom, MIN_SIDEBAR_HEIGHT)

    @split_bottom.setter
    def split_bottom(self, value: int) -> None:
        self.set(self.K.split_bottom, value)
