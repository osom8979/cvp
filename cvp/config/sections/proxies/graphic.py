# -*- coding: utf-8 -*-

from typing import Optional

from overrides import override

from cvp.config.sections.graphic import GraphicConfig
from cvp.patterns.proxy import ValueProxy


class ForceEglProxy(ValueProxy[Optional[bool]]):
    def __init__(self, config: GraphicConfig):
        self._config = config

    @override
    def get(self) -> Optional[bool]:
        return self._config.force_egl

    @override
    def set(self, value: Optional[bool]) -> None:
        self._config.force_egl = value


class UseAccelerateProxy(ValueProxy[Optional[bool]]):
    def __init__(self, config: GraphicConfig):
        self._config = config

    @override
    def get(self) -> Optional[bool]:
        return self._config.use_accelerate

    @override
    def set(self, value: Optional[bool]) -> None:
        self._config.use_accelerate = value
