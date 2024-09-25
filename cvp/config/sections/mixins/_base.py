# -*- coding: utf-8 -*-

from typing import Protocol, runtime_checkable

from cvp.config._base import ValueT


@runtime_checkable
class SupportsBaseSection(Protocol):
    def has(self, key: str) -> bool: ...

    def get(self, key: str, default: ValueT, *, raw=False) -> ValueT: ...

    def set(self, key: str, value: ValueT) -> None: ...
