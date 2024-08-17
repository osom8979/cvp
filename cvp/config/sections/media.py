# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config._base import BaseConfig
from cvp.config.sections._window import CommonWindowSection


@unique
class Mode(StrEnum):
    file = auto()
    manual = auto()


@unique
class _Keys(StrEnum):
    name_ = "name"
    mode = auto()
    file = auto()
    cmds = auto()


class MediaSection(CommonWindowSection):
    K = _Keys

    def __init__(self, config: BaseConfig, section="media"):
        super().__init__(config=config, section=section)

    @property
    def name(self) -> str:
        return self.get(self.K.name_, str())

    @name.setter
    def name(self, value: str) -> None:
        self.set(self.K.name_, value)

    @property
    def mode(self) -> Mode:
        return Mode(self.get(self.K.mode, str(Mode.file)))

    @mode.setter
    def mode(self, value: Mode) -> None:
        self.set(self.K.mode, str(value))

    @property
    def file(self) -> str:
        return self.get(self.K.file, str())

    @file.setter
    def file(self, value: str) -> None:
        self.set(self.K.file, value)

    @property
    def cmds(self) -> str:
        return self.get(self.K.cmds, str())

    @cmds.setter
    def cmds(self, value: str) -> None:
        self.set(self.K.cmds, value)
