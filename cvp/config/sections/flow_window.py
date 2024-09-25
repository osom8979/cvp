# -*- coding: utf-8 -*-

from enum import StrEnum, unique

from cvp.config.sections._base import BaseSection
from cvp.config.sections.mixins.cutting_edge import CuttingEdgeSectionMixin
from cvp.config.sections.mixins.window import WindowSectionMixin


@unique
class _Keys(StrEnum):
    pass


class FlowWindowSection(BaseSection, CuttingEdgeSectionMixin, WindowSectionMixin):
    K = _Keys
