# -*- coding: utf-8 -*-

from typing import Sequence

from cvp.context.context import Context
from cvp.renderer.popup.popup import Popup
from cvp.renderer.popup.popup_propagator import PopupPropagator
from cvp.types.override import override
from cvp.windows.preference._base import PreferenceWidget
from cvp.windows.preference.ffmpeg.exe import ExeTabs


class FFmpegPreference(PopupPropagator, PreferenceWidget):
    def __init__(self, context: Context, label="FFmpeg"):
        self._config = context.config.ffmpeg
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
