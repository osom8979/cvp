# -*- coding: utf-8 -*-

from overrides import override

from cvp.config.sections.flow import FlowAuiConfig
from cvp.patterns.proxy import ValueProxy


class SplitTreeProxy(ValueProxy[float]):
    def __init__(self, section: FlowAuiConfig):
        self._section = section

    @override
    def get(self) -> float:
        return self._section.split_tree

    @override
    def set(self, value: float) -> None:
        self._section.split_tree = value
