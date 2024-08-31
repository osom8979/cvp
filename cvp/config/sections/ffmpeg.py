# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config._base import BaseConfig
from cvp.config.sections._base import BaseSection
from cvp.variables import MAX_STREAM_LOGGING_HISTORY_LINES


@unique
class _Keys(StrEnum):
    ffmpeg = auto()
    ffprobe = auto()
    logging_history = auto()
    logging_encoding = auto()


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

    @property
    def logging_history(self) -> int:
        return self.get(self.K.logging_history, MAX_STREAM_LOGGING_HISTORY_LINES)

    @logging_history.setter
    def logging_history(self, value: int) -> None:
        self.set(self.K.logging_history, value)

    @property
    def logging_encoding(self) -> str:
        return self.get(self.K.logging_encoding, "utf-8")

    @logging_encoding.setter
    def logging_encoding(self, value: str) -> None:
        self.set(self.K.logging_encoding, value)
