# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config._base import BaseConfig
from cvp.config.sections._base import BaseSection


@unique
class _Keys(StrEnum):
    ffmpeg = auto()
    ffprobe = auto()


class FFmpegSection(BaseSection):
    K = _Keys

    def __init__(self, config: BaseConfig, section="font"):
        super().__init__(config=config, section=section)

    @property
    def ffmpeg(self) -> str:
        return self.get(self.K.ffmpeg, "ffmpeg")

    @ffmpeg.setter
    def ffmpeg(self, value: str) -> None:
        self.set(self.K.ffmpeg, value)

    @property
    def ffprobe(self) -> str:
        return self.get(self.K.ffprobe, "ffprobe")

    @ffprobe.setter
    def ffprobe(self, value: str) -> None:
        self.set(self.K.ffprobe, value)
