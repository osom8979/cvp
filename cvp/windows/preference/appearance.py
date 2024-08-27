# -*- coding: utf-8 -*-

from cvp.types.override import override
from cvp.widgets.hoc.widget import WidgetInterface


class AppearancePreference(WidgetInterface):
    def __init__(self, label="Appearance"):
        self._label = label

    def __str__(self):
        return self._label

    @override
    def on_process(self) -> None:
        pass
