# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config._base import BaseConfig
from cvp.config.sections._base import BaseSection


@unique
class _Keys(StrEnum):
    force_egl = auto()


class GraphicSection(BaseSection):
    K = _Keys

    def __init__(self, config: BaseConfig, section="graphic"):
        super().__init__(config=config, section=section)

    @property
    def force_egl(self) -> bool:
        return self.get(self.K.force_egl, False)

    @force_egl.setter
    def force_egl(self, value: bool) -> None:
        self.set(self.K.force_egl, value)
