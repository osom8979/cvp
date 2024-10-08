# -*- coding: utf-8 -*-

from overrides import override

from cvp.config.sections.bases.aui import AuiWindowConfig
from cvp.patterns.proxy import ValueProxy


class AuiLeftProxy(ValueProxy[float]):
    def __init__(self, aui: AuiWindowConfig):
        self._aui = aui

    @override
    def get(self) -> float:
        return self._aui.split_left

    @override
    def set(self, value: float) -> None:
        self._aui.split_left = value


class AuiRightProxy(ValueProxy[float]):
    def __init__(self, aui: AuiWindowConfig):
        self._aui = aui

    @override
    def get(self) -> float:
        return self._aui.split_right

    @override
    def set(self, value: float) -> None:
        self._aui.split_right = value


class AuiBottomProxy(ValueProxy[float]):
    def __init__(self, aui: AuiWindowConfig):
        self._aui = aui

    @override
    def get(self) -> float:
        return self._aui.split_bottom

    @override
    def set(self, value: float) -> None:
        self._aui.split_bottom = value
