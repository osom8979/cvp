# -*- coding: utf-8 -*-

from datetime import datetime
from logging import DEBUG, Logger, getLogger
from typing import Final, Optional, Union

DEFAULT_THRESHOLD: Final[int] = 10_000

PROFILE_STRFMT_PREFIX: Final[str] = "[{prefix}] "
PROFILE_STRFMT_SUFFIX: Final[str] = "Step #{iter}, average duration: {average:.3f}s"

PROFILE_STRFMT_WITH_PREFIX: Final[str] = PROFILE_STRFMT_PREFIX + PROFILE_STRFMT_SUFFIX
PROFILE_STRFMT_NO_PREFIX: Final[str] = PROFILE_STRFMT_SUFFIX


class ProfileLogging:
    def __init__(
        self,
        logger: Optional[Union[str, Logger]] = None,
        threshold=DEFAULT_THRESHOLD,
        level=DEBUG,
        strfmt: Optional[str] = None,
        prefix: Optional[str] = None,
    ):
        self._logger = logger if isinstance(logger, Logger) else getLogger(logger)
        self._threshold = threshold
        self._level = level
        self._prefix = prefix

        self._begin = datetime.now()
        self._end = datetime.now()

        self._step_iteration = 0
        self._step_duration = 0.0

        self._total_iteration = 0
        self._total_duration = 0.0

        if strfmt:
            self._strfmt = strfmt
        else:
            if self._prefix:
                self._strfmt = PROFILE_STRFMT_WITH_PREFIX
            else:
                self._strfmt = PROFILE_STRFMT_NO_PREFIX

    @property
    def prefix(self):
        return self._prefix

    @property
    def step_iteration(self):
        return self._step_iteration

    @property
    def step_duration(self):
        return self._step_duration

    @property
    def step_average(self):
        return self._step_duration / self._step_iteration

    @property
    def total_iteration(self):
        return self._total_iteration

    @property
    def total_duration(self):
        return self._total_duration

    @property
    def total_average(self):
        return self._total_duration / self._total_iteration

    @property
    def duration(self):
        return self._end - self._begin

    @property
    def duration_seconds(self) -> float:
        return self.duration.total_seconds()

    def fmt(self) -> str:
        return self._strfmt.format(
            prefix=self.prefix,
            iter=self._total_iteration,
            average=self.step_average,
        )

    def is_emit(self) -> bool:
        return self._step_iteration % self._threshold == 0

    def logging(self) -> None:
        self._logger.log(self._level, self.fmt())

    def reset(self) -> None:
        self._step_iteration = 0
        self._step_duration = 0.0

    def begin(self, dt: Optional[datetime] = None, step=1) -> None:
        self._begin = dt if dt else datetime.now()
        self._step_iteration += step
        self._total_iteration += step

    def end(self, dt: Optional[datetime] = None) -> None:
        self._end = dt if dt else datetime.now()
        duration_seconds = self.duration_seconds
        self._step_duration += duration_seconds
        self._total_duration += duration_seconds

        if not self.is_emit():
            return

        self.logging()
        self.reset()

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()
