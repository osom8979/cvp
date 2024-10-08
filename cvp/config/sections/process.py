# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.config.sections.mixins.manager import ManagerMixin
from cvp.variables import PROCESS_TEARDOWN_TIMEOUT


@dataclass
class ProcessConfig(ManagerMixin):
    teardown_timeout: float = PROCESS_TEARDOWN_TIMEOUT
