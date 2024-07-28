# -*- coding: utf-8 -*-

from enum import StrEnum, unique

from cvp.config._base import BaseConfig
from cvp.config.sections._base import BaseSection


@unique
class _Keys(StrEnum):
    pass


class DefaultSection(BaseSection):
    K = _Keys

    def __init__(self, config: BaseConfig):
        super().__init__(config, section="DEFAULT")
