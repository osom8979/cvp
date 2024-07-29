# -*- coding: utf-8 -*-

from typing import Optional, Union, overload

from cvp.config._base import BaseConfig, _DefaultT


class BaseSection:
    def __init__(self, config: BaseConfig, section: str):
        self._config = config
        self._section = section

    @property
    def section(self) -> str:
        return self._section

    # fmt: off
    @overload
    def get(self, key: str, default: str) -> str: ...
    @overload
    def get(self, key: str, default: bool) -> bool: ...
    @overload
    def get(self, key: str, default: int) -> int: ...
    @overload
    def get(self, key: str, default: float) -> float: ...
    # fmt: on

    def get(
        self,
        key: str,
        default: _DefaultT,
    ) -> Optional[Union[str, bool, int, float]]:
        return self._config.get(self._section, key, default)

    def set(self, key: str, value: _DefaultT) -> None:
        self._config.set(self._section, key, value)
