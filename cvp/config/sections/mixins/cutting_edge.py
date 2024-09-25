# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config.sections.mixins._base import SupportsBaseSection
from cvp.variables import MIN_SIDEBAR_HEIGHT, MIN_SIDEBAR_WIDTH


@unique
class Keys(StrEnum):
    split_left = auto()
    split_right = auto()
    split_bottom = auto()


class CuttingEdgeSectionMixin(SupportsBaseSection):
    @property
    def has_split_left(self) -> bool:
        return self.has(Keys.split_left)

    @property
    def split_left(self) -> float:
        return self.get(Keys.split_left, MIN_SIDEBAR_WIDTH)

    @split_left.setter
    def split_left(self, value: float) -> None:
        self.set(Keys.split_left, value)

    @property
    def has_split_right(self) -> bool:
        return self.has(Keys.split_right)

    @property
    def split_right(self) -> float:
        return self.get(Keys.split_right, MIN_SIDEBAR_WIDTH)

    @split_right.setter
    def split_right(self, value: float) -> None:
        self.set(Keys.split_right, value)

    @property
    def has_split_bottom(self) -> bool:
        return self.has(Keys.split_bottom)

    @property
    def split_bottom(self) -> float:
        return self.get(Keys.split_bottom, MIN_SIDEBAR_HEIGHT)

    @split_bottom.setter
    def split_bottom(self, value: float) -> None:
        self.set(Keys.split_bottom, value)
