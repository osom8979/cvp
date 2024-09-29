# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config.sections._base import BaseSection
from cvp.config.sections.mixins.cutting_edge import CuttingEdgeSectionMixin
from cvp.config.sections.mixins.window import WindowSectionMixin
from cvp.variables import MIN_SIDEBAR_HEIGHT


@unique
class _Keys(StrEnum):
    split_tree = auto()


class FlowWindowSection(BaseSection, CuttingEdgeSectionMixin, WindowSectionMixin):
    K = _Keys

    @property
    def has_split_tree(self) -> bool:
        return self.has(self.K.split_tree)

    @property
    def split_tree(self) -> float:
        return self.get(self.K.split_tree, float(MIN_SIDEBAR_HEIGHT))

    @split_tree.setter
    def split_tree(self, value: float) -> None:
        self.set(self.K.split_tree, value)
