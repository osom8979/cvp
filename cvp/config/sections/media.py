# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import StrEnum, auto, unique
from typing import Tuple

from cvp.config.sections.mixins.window import WindowMixin


@unique
class Mode(StrEnum):
    file = auto()
    url = auto()
    manual = auto()


@dataclass
class MediaSection(WindowMixin):
    mode: Mode = Mode.file
    file: str = ""
    frame_width: int = 0
    frame_height: int = 0
    cmds: str = ""

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
