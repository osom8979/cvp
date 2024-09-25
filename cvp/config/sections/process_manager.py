# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config.sections._base import BaseSection
from cvp.config.sections.mixins.manager import ManagerSectionMixin
from cvp.variables import PROCESS_TEARDOWN_TIMEOUT


@unique
class _Keys(StrEnum):
    teardown_timeout = auto()


class ProcessManagerSection(BaseSection, ManagerSectionMixin):
    K = _Keys

    @property
    def teardown_timeout(self) -> float:
        return self.get(self.K.teardown_timeout, PROCESS_TEARDOWN_TIMEOUT)

    @teardown_timeout.setter
    def teardown_timeout(self, value: float) -> None:
        self.set(self.K.teardown_timeout, value)
