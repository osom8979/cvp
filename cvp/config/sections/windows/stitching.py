# -*- coding: utf-8 -*-

from enum import StrEnum, unique

from cvp.config._base import BaseConfig
from cvp.config.sections.windows._base import BaseWindowSection


@unique
class _Keys(StrEnum):
    pass


class StitchingSection(BaseWindowSection):
    K = _Keys

    def __init__(self, config: BaseConfig, section="stitching"):
        super().__init__(config=config, section=section)
