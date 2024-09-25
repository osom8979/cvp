# -*- coding: utf-8 -*-

from enum import StrEnum, unique

from cvp.config.sections._base import BaseSection
from cvp.config.sections.mixins.manager import ManagerSectionMixin


@unique
class _Keys(StrEnum):
    pass


class LayoutManagerSection(BaseSection, ManagerSectionMixin):
    K = _Keys
