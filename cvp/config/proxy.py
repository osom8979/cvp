# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Generic

from cvp.config._base import ValueT


class ValueProxy(Generic[ValueT], ABC):
    @abstractmethod
    def set(self, value: ValueT) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self) -> ValueT:
        raise NotImplementedError
