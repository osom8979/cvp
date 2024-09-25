# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config.sections._base import BaseSection


@unique
class _Keys(StrEnum):
    config_path = auto()
    root_severity = auto()


class LoggingSection(BaseSection):
    K = _Keys

    @property
    def has_config_path(self) -> bool:
        return self.has(self.K.config_path)

    @property
    def config_path(self) -> str:
        return self.get(self.K.config_path, str())

    @config_path.setter
    def config_path(self, value: str) -> None:
        self.set(self.K.config_path, value)

    @property
    def root_severity(self) -> str:
        return self.get(self.K.root_severity, str())

    @root_severity.setter
    def root_severity(self, value: str) -> None:
        self.set(self.K.root_severity, value)
