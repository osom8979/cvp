# -*- coding: utf-8 -*-

from typing import Generic

from cvp.config._base import ValueT


class ValueProxy(Generic[ValueT]):
    def has(self) -> bool:
        raise NotImplementedError

    def get(self) -> ValueT:
        raise NotImplementedError

    def set(self, value: ValueT) -> None:
        raise NotImplementedError
