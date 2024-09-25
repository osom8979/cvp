# -*- coding: utf-8 -*-

from enum import StrEnum, unique

from cvp.config.sections._base import BaseSection


@unique
class _Keys(StrEnum):
    pass


class LayoutSection(BaseSection):
    K = _Keys
