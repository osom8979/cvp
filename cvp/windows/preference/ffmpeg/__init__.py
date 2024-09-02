# -*- coding: utf-8 -*-

from shutil import which
from typing import Optional, Sequence
from weakref import ref

import imgui

from cvp.config.sections.ffmpeg import FFmpegSection
from cvp.popups.open_file import OpenFilePopup
from cvp.process.manager import ProcessManager
from cvp.types import override
from cvp.widgets import button_ex, input_text_value
from cvp.widgets.hoc.popup import Popup, PopupPropagator
from cvp.widgets.hoc.widget import WidgetInterface


class FFmpegPreference(PopupPropagator, WidgetInterface):
    def __init__(self, section: FFmpegSection, pm: ProcessManager, label="FFmpeg"):
        self._section = section
        self._pm = ref(pm)
        self._label = label
        self._ffmpeg_browser = OpenFilePopup(
            "Select ffmpeg executable",
            target=self.on_ffmpeg_file,
        )
        self._ffprobe_browser = OpenFilePopup(
            "Select ffprobe executable",
            target=self.on_ffprobe_file,
        )

    def __str__(self):
        return self._label

    @property
    def pm(self) -> Optional[ProcessManager]:
        return self._pm()

    @property
    @override
    def popups(self) -> Sequence[Popup]:
        return [self._ffmpeg_browser, self._ffprobe_browser]

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

    def on_ffmpeg_file(self, file: str) -> None:
        self.ffmpeg = file

    def on_ffprobe_file(self, file: str) -> None:
        self.ffprobe = file

    @staticmethod
    def exe_group(name: str, path: str, browser: OpenFilePopup) -> str:
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
            browser.show()

        return path

    @override
    def on_process(self) -> None:
        self.ffmpeg = self.exe_group("ffmpeg", self.ffmpeg, self._ffmpeg_browser)
        imgui.separator()
        self.ffprobe = self.exe_group("ffprobe", self.ffprobe, self._ffprobe_browser)
