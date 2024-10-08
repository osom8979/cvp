# -*- coding: utf-8 -*-

from overrides import override

from cvp.config.sections.ffmpeg import FFmpegConfig
from cvp.patterns.proxy import ValueProxy


class FFmpegProxy(ValueProxy[str]):
    def __init__(self, section: FFmpegConfig):
        self._section = section

    @override
    def get(self) -> str:
        return self._section.ffmpeg

    @override
    def set(self, value: str) -> None:
        self._section.ffmpeg = value


class FFprobeProxy(ValueProxy[str]):
    def __init__(self, section: FFmpegConfig):
        self._section = section

    @override
    def get(self) -> str:
        return self._section.ffprobe

    @override
    def set(self, value: str) -> None:
        self._section.ffprobe = value
