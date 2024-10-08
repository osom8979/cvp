# -*- coding: utf-8 -*-

from overrides import override

from cvp.config.sections.mixins.sidebar import SidebarMixin
from cvp.patterns.proxy import ValueProxy


class SidebarWidthProxy(ValueProxy[float]):
    def __init__(self, sidebar: SidebarMixin):
        self._sidebar = sidebar

    @override
    def get(self) -> float:
        return self._sidebar.sidebar_width

    @override
    def set(self, value: float) -> None:
        self._sidebar.sidebar_width = value
