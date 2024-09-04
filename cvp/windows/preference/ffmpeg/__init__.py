# -*- coding: utf-8 -*-

from typing import Sequence

from cvp.types import override
from cvp.widgets.hoc.popup import Popup, PopupPropagator
from cvp.widgets.hoc.widget import WidgetInterface
from cvp.windows.preference.ffmpeg.exe import ExeTabs


class FFmpegPreference(PopupPropagator, WidgetInterface):
    def __init__(self, label="FFmpeg"):
        self._section = self.propagated_context().config.ffmpeg
        self._label = label
        self._tabs = ExeTabs()

    def __str__(self):
        return self._label

    @property
    @override
    def popups(self) -> Sequence[Popup]:
        return self._tabs.popups

    @override
    def on_process(self) -> None:
        self._tabs.do_process()
