# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config._base import BaseConfig
from cvp.config.sections._base import BaseSection


@unique
class _Keys(StrEnum):
    debug = auto()
    verbose = auto()


class DeveloperSection(BaseSection):
    K = _Keys

    def __init__(self, config: BaseConfig, section="developer"):
        super().__init__(config=config, section=section)

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
