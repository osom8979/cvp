# -*- coding: utf-8 -*-

from typing import Generic, TypeVar

from cvp.context.context import Context
from cvp.logging.logging import logger
from cvp.patterns.proxy import ValueProxy, ValueT

ErrorT = TypeVar("ErrorT", bound=BaseException)


class AutoFixerError(Generic[ValueT], Exception):
    def __init__(self, path: str, value: ValueT):
        super().__init__(
            f"Due to AutoFixer, '{path}' was automatically corrected to {value}"
        )


class AutoFixer(Generic[ValueT, ErrorT]):
    def __init__(
        self,
        context: Context,
        path: str,
        proxy: ValueProxy[ValueT],
        not_exists_value: ValueT,
        update_value: ValueT,
    ):
        self._context = context
        self._path = path
        self._proxy = proxy
        self._not_exists_value = not_exists_value
        self._update_value = update_value

    def run(self, error: ErrorT) -> None:
        logger.warning(
            f"Please modify the value of '{self._path}' to {self._update_value}"
            f" section of the '{str(self._context.home.cvp_yml)}' file and try again."
        )

        if (
            not self._context.readonly
            and self._context.config.context.auto_fixer
            and self._proxy.get() is self._not_exists_value
        ):
            try:
                self._context.validate_writable_home()
            except BaseException as e1:
                logger.error(e1)
            else:
                try:
                    self._proxy.set(self._update_value)
                    self._context.save_config_unsafe()
                except BaseException as e2:
                    logger.error(e2)
                else:
                    raise AutoFixerError[ValueT](
                        self._path, self._update_value
                    ) from error

        raise RuntimeError(
            f"An issue has occurred with the '{self._path}' features"
        ) from error
