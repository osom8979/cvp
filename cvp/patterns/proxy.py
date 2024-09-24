# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from cvp.types import override

ValueT = TypeVar("ValueT")


class ValueProxy(Generic[ValueT], ABC):
    @abstractmethod
    def has(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get(self) -> ValueT:
        raise NotImplementedError

    @abstractmethod
    def set(self, value: ValueT) -> None:
        raise NotImplementedError


class PropertyProxy(ValueProxy[ValueT]):
    def __init__(self, obj: Any, key: str):
        self._obj = obj
        self._key = key

    @override
    def has(self) -> bool:
        return hasattr(self._obj, self._key)

    @override
    def get(self) -> ValueT:
        return getattr(self._obj, self._key)

    @override
    def set(self, value: ValueT) -> None:
        setattr(self._obj, self._key, value)
