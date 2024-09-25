# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from cvp.config.sections._base import BaseSection
from cvp.variables import MAX_PROCESS_WORKERS, MAX_THREAD_WORKERS


@unique
class _Keys(StrEnum):
    thread_workers = auto()
    process_workers = auto()


class ConcurrencySection(BaseSection):
    K = _Keys

    @property
    def thread_workers(self) -> int:
        return self.get(self.K.thread_workers, MAX_THREAD_WORKERS)

    @thread_workers.setter
    def thread_workers(self, value: int) -> None:
        self.set(self.K.thread_workers, value)

    @property
    def process_workers(self) -> int:
        return self.get(self.K.process_workers, MAX_PROCESS_WORKERS)

    @process_workers.setter
    def process_workers(self, value: int) -> None:
        self.set(self.K.process_workers, value)
