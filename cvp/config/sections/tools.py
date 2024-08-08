# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config._base import BaseConfig
from cvp.config.sections._base import BaseSection


@unique
class _Keys(StrEnum):
    demo = auto()
    av = auto()


class ToolsSection(BaseSection):
    K = _Keys

    def __init__(self, config: BaseConfig, section="tools"):
        super().__init__(config=config, section=section)

    @property
    def demo(self) -> bool:
        return self.get(self.K.demo, False)

    @demo.setter
    def demo(self, value: bool) -> None:
        self.set(self.K.demo, value)

    @property
    def av(self) -> bool:
        return self.get(self.K.av, False)

    @av.setter
    def av(self, value: bool) -> None:
        self.set(self.K.av, value)
