# -*- coding: utf-8 -*-

from typing import Generic, TypeVar

# noinspection PyProtectedMember
from cvp.config._base import ValueT

# noinspection PyProtectedMember
from cvp.config.sections._base import BaseSection
from cvp.context.context import Context
from cvp.logging.logging import logger

ErrorT = TypeVar("ErrorT", bound=BaseException)


class AutoFixerError(Generic[ValueT], Exception):
    def __init__(self, section: str, option: str, value: ValueT):
        value_text = f"'{value}'" if isinstance(value, str) else str(value)
        super().__init__(
            "Due to AutoFixer, "
            f"'{option}' in [{section}] was automatically corrected to {value_text}"
        )


class AutoFixer(Generic[ValueT, ErrorT]):
    _value: ValueT

    def __init__(
        self,
        context: Context,
        section: BaseSection,
        option: str,
        value: ValueT,
    ):
        self._context = context
        self._section = section
        self._option = option
        self._value = value

    def run(self, error: ErrorT) -> None:
        section = self._section.section
        option = self._option

        if isinstance(self._value, str):
            value = f"'{str(self._value)}'"
        else:
            value = str(self._value)

        logger.warning(
            f"Please modify the value of '{option}' to {value} in the [{section}]"
            f" section of the '{str(self._context.home.cvp_ini)}' file and try again."
        )

        if (
            not self._context.readonly
            and self._context.config.context.auto_fixer
            and not self._section.has(self._option)
        ):
            try:
                self._context.validate_writable_home()
            except BaseException as e1:
                logger.error(e1)
            else:
                try:
                    self._section.set(self._option, self._value)
                    self._context.save_config_unsafe()
                except BaseException as e2:
                    logger.error(e2)
                else:
                    raise AutoFixerError[ValueT](
                        section, option, self._value
                    ) from error

        raise RuntimeError(
            f"An issue has occurred with the '{option}' features "
            f"in the [{section}] section"
        ) from error
