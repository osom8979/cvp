# -*- coding: utf-8 -*-

from enum import StrEnum, unique

from cvp.config._base import BaseConfig
from cvp.config.sections.windows.manager._base import BaseManagerSection


@unique
class _Keys(StrEnum):
    pass


class FlowManagerSection(BaseManagerSection):
    K = _Keys

    def __init__(self, config: BaseConfig, section="flow_manager"):
        super().__init__(config=config, section=section)