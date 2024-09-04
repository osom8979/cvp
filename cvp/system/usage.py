# -*- coding: utf-8 -*-

from time import time
from typing import NamedTuple, Optional

from psutil import cpu_percent, virtual_memory


class Percentage(NamedTuple):
    cpu: float
    vmem: float


class SystemUsage:
    def __init__(self, interval: Optional[float] = None):
        self.interval = interval

        self._latest_cpu_usage = 0.0
        self._latest_vmem_usage = 0.0
        self._latest_time = time()

    @property
    def percentage(self) -> Percentage:
        return Percentage(self._latest_cpu_usage, self._latest_vmem_usage)

    def update(self, update_time: Optional[float] = None) -> Percentage:
        self._latest_cpu_usage = cpu_percent(interval=None)
        self._latest_vmem_usage = virtual_memory().percent
        self._latest_time = update_time if update_time is not None else time()
        return self.percentage

    def update_interval(self) -> Percentage:
        current = time()

        if self.interval is not None:
            if current - self._latest_time < self.interval:
                return self.percentage

        return self.update(current)
