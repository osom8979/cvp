# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import StrEnum, auto, unique
from typing import Tuple

from cvp.config.sections.bases.manager import ManagerWindowConfig
from cvp.config.sections.bases.window import WindowConfig


@unique
class Mode(StrEnum):
    file = auto()
    url = auto()
    manual = auto()


@dataclass
class MediaWindowConfig(WindowConfig):
    mode: Mode = Mode.file
    file: str = field(default_factory=str)
    cmds: str = field(default_factory=str)
    frame_width: int = 0
    frame_height: int = 0

    def set_file_mode(self) -> None:
        self.mode = Mode.file

    def set_url_mode(self) -> None:
        self.mode = Mode.url

    def set_manual_mode(self) -> None:
        self.mode = Mode.manual

    @property
    def frame_size(self) -> Tuple[int, int]:
        return self.frame_width, self.frame_height

    @frame_size.setter
    def frame_size(self, value: Tuple[int, int]) -> None:
        self.frame_width = value[0]
        self.frame_height = value[1]


@dataclass
class MediaManagerConfig(ManagerWindowConfig):
    pass
