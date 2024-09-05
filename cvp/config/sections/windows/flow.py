# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config._base import BaseConfig
from cvp.config.sections.windows._base import BaseWindowSection


@unique
class _Keys(StrEnum):
    type_ = "type"
    class_ = "class"
    x = auto()
    y = auto()
    width = auto()
    height = auto()


class FlowSection(BaseWindowSection):
    K = _Keys

    def __init__(self, config: BaseConfig, section="media"):
        super().__init__(config=config, section=section)
