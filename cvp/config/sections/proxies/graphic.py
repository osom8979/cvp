# -*- coding: utf-8 -*-

from typing import Optional

from overrides import override

from cvp.config.sections.graphic import GraphicConfig
from cvp.patterns.proxy import ValueProxy


class ForceEglProxy(ValueProxy[Optional[bool]]):
    def __init__(self, section: GraphicConfig):
        self._section = section

    @override
    def get(self) -> Optional[bool]:
        return self._section.force_egl

    @override
    def set(self, value: Optional[bool]) -> None:
        self._section.force_egl = value


class UseAccelerateProxy(ValueProxy[Optional[bool]]):
    def __init__(self, section: GraphicConfig):
        self._section = section

    @override
    def get(self) -> Optional[bool]:
        return self._section.use_accelerate

    @override
    def set(self, value: Optional[bool]) -> None:
        self._section.use_accelerate = value
