# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from overrides import override

from cvp.config._base import BaseConfig
from cvp.config.proxy import ValueProxy
from cvp.config.sections._base import BaseSection
from cvp.variables import STREAM_LOGGING_MAXSIZE, STREAM_LOGGING_NEWLINE_SIZE


@unique
class _Keys(StrEnum):
    ffmpeg = auto()
    ffprobe = auto()
    logging_maxsize = auto()
    logging_encoding = auto()
    logging_newline_size = auto()


class FFmpegSection(BaseSection):
    K = _Keys

    def __init__(self, config: BaseConfig, section="ffmpeg"):
        super().__init__(config=config, section=section)

    @property
    def has_ffmpeg(self) -> bool:
        return self.has(self.K.ffmpeg)

    @property
    def ffmpeg(self) -> str:
        return self.get(self.K.ffmpeg, "ffmpeg")

    @ffmpeg.setter
    def ffmpeg(self, value: str) -> None:
        self.set(self.K.ffmpeg, value)

    @property
    def has_ffprobe(self) -> bool:
        return self.has(self.K.ffprobe)

    @property
    def ffprobe(self) -> str:
        return self.get(self.K.ffprobe, "ffprobe")

    @ffprobe.setter
    def ffprobe(self, value: str) -> None:
        self.set(self.K.ffprobe, value)

    @property
    def logging_maxsize(self) -> int:
        return self.get(self.K.logging_maxsize, STREAM_LOGGING_MAXSIZE)

    @logging_maxsize.setter
    def logging_maxsize(self, value: int) -> None:
        self.set(self.K.logging_maxsize, value)

    @property
    def logging_encoding(self) -> str:
        return self.get(self.K.logging_encoding, "utf-8")

    @logging_encoding.setter
    def logging_encoding(self, value: str) -> None:
        self.set(self.K.logging_encoding, value)

    @property
    def logging_newline_size(self) -> int:
        return self.get(self.K.logging_newline_size, STREAM_LOGGING_NEWLINE_SIZE)

    @logging_newline_size.setter
    def logging_newline_size(self, value: int) -> None:
        self.set(self.K.logging_newline_size, value)


class FFmpegProxy(ValueProxy[str]):
    def __init__(self, section: FFmpegSection):
        self._section = section

    @override
    def has(self) -> bool:
        return self._section.has_ffmpeg

    @override
    def get(self) -> str:
        return self._section.ffmpeg

    @override
    def set(self, value: str) -> None:
        self._section.ffmpeg = value


class FFprobeProxy(ValueProxy[str]):
    def __init__(self, section: FFmpegSection):
        self._section = section

    @override
    def has(self) -> bool:
        return self._section.has_ffprobe

    @override
    def get(self) -> str:
        return self._section.ffprobe

    @override
    def set(self, value: str) -> None:
        self._section.ffprobe = value
