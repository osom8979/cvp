# -*- coding: utf-8 -*-

from enum import StrEnum, unique

from cvp.config._base import BaseConfig
from cvp.config.sections.commons.window import CommonWindowSection


@unique
class _Keys(StrEnum):
    pass


class DemoSection(CommonWindowSection):
    K = _Keys

    def __init__(self, config: BaseConfig, section="demo"):
        super().__init__(config=config, section=section)
