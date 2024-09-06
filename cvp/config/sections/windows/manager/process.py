# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config._base import BaseConfig
from cvp.config.sections.windows.manager._base import BaseManagerSection
from cvp.variables import PROCESS_TEARDOWN_TIMEOUT


@unique
class _Keys(StrEnum):
    teardown_timeout = auto()


class ProcessManagerSection(BaseManagerSection):
    K = _Keys

    def __init__(self, config: BaseConfig, section="process_manager"):
        super().__init__(config=config, section=section)

    @property
    def teardown_timeout(self) -> float:
        return self.get(self.K.teardown_timeout, PROCESS_TEARDOWN_TIMEOUT)

    @teardown_timeout.setter
    def teardown_timeout(self, value: float) -> None:
        self.set(self.K.teardown_timeout, value)
