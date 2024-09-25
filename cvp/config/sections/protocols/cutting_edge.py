# -*- coding: utf-8 -*-

from abc import abstractmethod
from typing import Protocol, TypeVar, runtime_checkable

_T = TypeVar("_T")


@runtime_checkable
class SupportsCuttingEdge(Protocol[_T]):
    __slots__ = ()

    @property
    @abstractmethod
    def split_left(self) -> _T: ...

    @split_left.setter
    @abstractmethod
    def split_left(self, value: _T) -> None: ...

    @property
    @abstractmethod
    def split_right(self) -> _T: ...

    @split_right.setter
    @abstractmethod
    def split_right(self, value: _T) -> None: ...

    @property
    @abstractmethod
    def split_bottom(self) -> _T: ...

    @split_bottom.setter
    @abstractmethod
    def split_bottom(self, value: _T) -> None: ...
