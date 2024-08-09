# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config._base import BaseConfig
from cvp.config.sections._window import CommonWindowSection


@unique
class _Keys(StrEnum):
    file = auto()
    name_ = "name"


class MediaSection(CommonWindowSection):
    K = _Keys

    def __init__(self, config: BaseConfig, section="media"):
        super().__init__(config=config, section=section)

    @property
    def file(self) -> str:
        return self.get(self.K.file, str())

    @file.setter
    def file(self, value: str) -> None:
        self.set(self.K.file, value)

    @property
    def name(self) -> str:
        return self.get(self.K.name_, str())

    @name.setter
    def name(self, value: str) -> None:
        self.set(self.K.name_, value)
