# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config.sections.mixins._base import SupportsBaseSection


@unique
class Keys(StrEnum):
    selected = auto()


class SelectedSectionMixin(SupportsBaseSection):
    @property
    def has_selected(self) -> bool:
        return self.has(Keys.selected)

    @property
    def selected(self) -> str:
        return self.get(Keys.selected, str())

    @selected.setter
    def selected(self, value: str) -> None:
        self.set(Keys.selected, value)
