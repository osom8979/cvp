# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config.sections._base import BaseSection


@unique
class _Keys(StrEnum):
    debug = auto()
    verbose = auto()
    metrics = auto()
    style = auto()
    demo = auto()


class DeveloperSection(BaseSection):
    K = _Keys

    @property
    def has_debug(self) -> bool:
        return self.has(self.K.debug)

    @property
    def debug(self) -> bool:
        return self.get(self.K.debug, False)

    @debug.setter
    def debug(self, value: bool) -> None:
        self.set(self.K.debug, value)

    @property
    def has_verbose(self) -> bool:
        return self.has(self.K.verbose)

    @property
    def verbose(self) -> int:
        return self.get(self.K.verbose, 0)

    @verbose.setter
    def verbose(self, value: int) -> None:
        self.set(self.K.verbose, value)

    @property
    def metrics(self) -> bool:
        return self.get(self.K.metrics, False)

    @metrics.setter
    def metrics(self, value: bool) -> None:
        self.set(self.K.metrics, value)

    @property
    def style(self) -> bool:
        return self.get(self.K.style, False)

    @style.setter
    def style(self, value: bool) -> None:
        self.set(self.K.style, value)

    @property
    def demo(self) -> bool:
        return self.get(self.K.demo, False)

    @demo.setter
    def demo(self, value: bool) -> None:
        self.set(self.K.demo, value)
