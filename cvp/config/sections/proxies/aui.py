# -*- coding: utf-8 -*-

from overrides import override

from cvp.config.sections.bases.aui import AuiWindowConfig
from cvp.patterns.proxy import ValueProxy


class AuiLeftProxy(ValueProxy[float]):
    def __init__(self, config: AuiWindowConfig):
        self._config = config

    @override
    def get(self) -> float:
        return self._config.split_left

    @override
    def set(self, value: float) -> None:
        self._config.split_left = value


class AuiRightProxy(ValueProxy[float]):
    def __init__(self, config: AuiWindowConfig):
        self._config = config

    @override
    def get(self) -> float:
        return self._config.split_right

    @override
    def set(self, value: float) -> None:
        self._config.split_right = value


class AuiBottomProxy(ValueProxy[float]):
    def __init__(self, config: AuiWindowConfig):
        self._config = config

    @override
    def get(self) -> float:
        return self._config.split_bottom

    @override
    def set(self, value: float) -> None:
        self._config.split_bottom = value
