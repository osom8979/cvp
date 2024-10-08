# -*- coding: utf-8 -*-

from overrides import override

from cvp.config.sections.ffmpeg import FFmpegConfig
from cvp.patterns.proxy import ValueProxy


class FFmpegProxy(ValueProxy[str]):
    def __init__(self, config: FFmpegConfig):
        self._config = config

    @override
    def get(self) -> str:
        return self._config.ffmpeg

    @override
    def set(self, value: str) -> None:
        self._config.ffmpeg = value


class FFprobeProxy(ValueProxy[str]):
    def __init__(self, config: FFmpegConfig):
        self._config = config

    @override
    def get(self) -> str:
        return self._config.ffprobe

    @override
    def set(self, value: str) -> None:
        self._config.ffprobe = value
