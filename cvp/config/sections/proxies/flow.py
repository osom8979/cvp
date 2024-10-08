# -*- coding: utf-8 -*-

from overrides import override

from cvp.config.sections.flow import FlowAuiConfig
from cvp.patterns.proxy import ValueProxy


class SplitTreeProxy(ValueProxy[float]):
    def __init__(self, config: FlowAuiConfig):
        self._config = config

    @override
    def get(self) -> float:
        return self._config.split_tree

    @override
    def set(self, value: float) -> None:
        self._config.split_tree = value
