# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config.sections.mixins._base import SupportsBaseSection


@unique
class Keys(StrEnum):
    sidebar_width = auto()
    sidebar_height = auto()


class SidebarWidthSectionMixin(SupportsBaseSection):
    @property
    def has_sidebar_width(self) -> bool:
        return self.has(Keys.sidebar_width)

    @property
    def sidebar_width(self) -> float:
        return self.get(Keys.sidebar_width, 0.0)

    @sidebar_width.setter
    def sidebar_width(self, value: float) -> None:
        self.set(Keys.sidebar_width, value)


class SidebarHeightSectionMixin(SupportsBaseSection):
    @property
    def has_sidebar_height(self) -> bool:
        return self.has(Keys.sidebar_height)

    @property
    def sidebar_height(self) -> float:
        return self.get(Keys.sidebar_height, 0.0)

    @sidebar_height.setter
    def sidebar_height(self, value: float) -> None:
        self.set(Keys.sidebar_height, value)


class SidebarSizeSectionMixin(SidebarWidthSectionMixin, SidebarHeightSectionMixin):
    pass
