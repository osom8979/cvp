# -*- coding: utf-8 -*-

from cvp.config.sections.ffmpeg import FFmpegSection
from cvp.process.helper.ffmpeg import FFmpegProcessHelper
from cvp.process.mapper import ProcessMapper
from cvp.process.process import Process
from cvp.resources.home import HomeDir


class ProcessManager(ProcessMapper[str, Process]):
    def __init__(self, section: FFmpegSection, home: HomeDir):
        super().__init__()
        self._ffmpeg = FFmpegProcessHelper(section=section, home=home)

    def spawn_ffmpeg_with_file(self, key: str, file: str, width: int, height: int):
        if self.__contains__(key):
            raise KeyError(f"Key is exists: '{key}'")

        process = self._ffmpeg.spawn_with_file(key, file, width, height)
        self.__setitem__(key, process)
        return process
