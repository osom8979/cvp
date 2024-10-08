# -*- coding: utf-8 -*-

from overrides import override

from cvp.config.sections.bases.sidebar import SidebarWindowConfig
from cvp.patterns.proxy import ValueProxy


class SidebarWidthProxy(ValueProxy[float]):
    def __init__(self, config: SidebarWindowConfig):
        self._config = config

    @override
    def get(self) -> float:
        return self._config.sidebar_width

    @override
    def set(self, value: float) -> None:
        self._config.sidebar_width = value
