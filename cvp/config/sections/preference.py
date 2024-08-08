# -*- coding: utf-8 -*-

from enum import StrEnum, unique

from cvp.config._base import BaseConfig
from cvp.config.sections._window import CommonWindowSection


@unique
class _Keys(StrEnum):
    pass


class PreferenceSection(CommonWindowSection):
    K = _Keys

    def __init__(self, config: BaseConfig, section="preference"):
        super().__init__(config=config, section=section)
