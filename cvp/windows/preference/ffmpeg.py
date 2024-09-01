# -*- coding: utf-8 -*-

from shutil import which

import imgui

from cvp.config.sections.ffmpeg import FFmpegSection
from cvp.popups.open_file import OpenFilePopup
from cvp.types import override
from cvp.widgets import button_ex, input_text_value
from cvp.widgets.hoc.widget import WidgetInterface


class FFmpegPreference(WidgetInterface):
    def __init__(self, section: FFmpegSection, label="FFmpeg"):
        self._section = section
        self._label = label
        self._ffmpeg_open = OpenFilePopup()
        self._ffprobe_open = OpenFilePopup()

    def __str__(self):
        return self._label

    @property
    def ffmpeg(self) -> str:
        return self._section.ffmpeg

    @ffmpeg.setter
    def ffmpeg(self, value: str) -> None:
        self._section.ffmpeg = value

    @property
    def ffprobe(self) -> str:
        return self._section.ffprobe

    @ffprobe.setter
    def ffprobe(self, value: str) -> None:
        self._section.ffprobe = value

    @staticmethod
    def exe_group(name: str, path: str, browse: OpenFilePopup) -> str:
        imgui.text(f"{name} executable")
        path = input_text_value(f"##{name}Path", path)

        if imgui.button(f"Default##{name}Default"):
            path = name
        imgui.same_line()
        which_path = which(name)
        if button_ex(f"Which##{name}Which", disabled=not which_path):
            assert isinstance(which_path, str)
            path = which_path
        imgui.same_line()
        if imgui.button(f"Cache##{name}Cache"):
            pass
        imgui.same_line()
        if imgui.button(f"Browse##{name}Browse"):
            browse.show()

        result = browse.do_process()
        if result:
            path = result

        return path

    @override
    def on_process(self) -> None:
        self.ffmpeg = self.exe_group("ffmpeg", self.ffmpeg, self._ffmpeg_open)
        imgui.separator()
        self.ffprobe = self.exe_group("ffprobe", self.ffprobe, self._ffprobe_open)
