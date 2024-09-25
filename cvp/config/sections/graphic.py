# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config.sections._base import BaseSection


@unique
class _Keys(StrEnum):
    force_egl = auto()
    use_accelerate = auto()


class GraphicSection(BaseSection):
    K = _Keys

    @property
    def has_force_egl(self) -> bool:
        return self.has(self.K.force_egl)

    @property
    def force_egl(self) -> bool:
        return self.get(self.K.force_egl, False)

    @force_egl.setter
    def force_egl(self, value: bool) -> None:
        self.set(self.K.force_egl, value)

    @property
    def force_egl_environ(self) -> str:
        return "1" if self.force_egl else "0"

    @property
    def has_use_accelerate(self) -> bool:
        return self.has(self.K.use_accelerate)

    @property
    def use_accelerate(self) -> bool:
        return self.get(self.K.use_accelerate, False)

    @use_accelerate.setter
    def use_accelerate(self, value: bool) -> None:
        self.set(self.K.use_accelerate, value)

    @property
    def use_accelerate_environ(self) -> str:
        return "1" if self.use_accelerate else "0"
