# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from typing import Tuple

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
    frame_width = auto()
    frame_height = auto()
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
    def frame_width(self) -> int:
        return self.get(self.K.frame_width, 0)

    @frame_width.setter
    def frame_width(self, value: int) -> None:
        self.set(self.K.frame_width, value)

    @property
    def frame_height(self) -> int:
        return self.get(self.K.frame_height, 0)

    @frame_height.setter
    def frame_height(self, value: int) -> None:
        self.set(self.K.frame_height, value)

    @property
    def frame_size(self) -> Tuple[int, int]:
        return self.frame_width, self.frame_height

    @frame_size.setter
    def frame_size(self, value: Tuple[int, int]) -> None:
        self.frame_width = value[0]
        self.frame_height = value[1]

    @property
    def cmds(self) -> str:
        return self.get(self.K.cmds, str())

    @cmds.setter
    def cmds(self, value: str) -> None:
        self.set(self.K.cmds, value)
