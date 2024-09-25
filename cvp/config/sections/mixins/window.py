# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config.sections.mixins._base import SupportsBaseSection


@unique
class Keys(StrEnum):
    opened = auto()
    title_ = "title"


class WindowSectionMixin(SupportsBaseSection):
    @property
    def has_opened(self) -> bool:
        return self.has(Keys.opened)

    @property
    def opened(self) -> bool:
        return self.get(Keys.opened, False)

    @opened.setter
    def opened(self, value: bool) -> None:
        self.set(Keys.opened, value)

    @property
    def has_title(self) -> bool:
        return self.has(Keys.title_)

    @property
    def title(self) -> str:
        return self.get(Keys.title_, str())

    @title.setter
    def title(self, value: str) -> None:
        self.set(Keys.title_, value)
