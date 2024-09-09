# -*- coding: utf-8 -*-

from typing import Sequence

from cvp.context import Context
from cvp.types import override
from cvp.widgets.hoc.popup import Popup, PopupPropagator
from cvp.windows.managers.preference._base import PreferenceWidget
from cvp.windows.managers.preference.ffmpeg.exe import ExeTabs


class FFmpegPreference(PopupPropagator, PreferenceWidget):
    def __init__(self, context: Context, label="FFmpeg"):
        self._section = context.config.ffmpeg
        self._label = label
        self._tabs = ExeTabs(context)

    @property
    @override
    def label(self) -> str:
        return self._label

    @property
    @override
    def popups(self) -> Sequence[Popup]:
        return self._tabs.popups

    @override
    def on_process(self) -> None:
        self._tabs.do_process()
