# -*- coding: utf-8 -*-

from abc import abstractmethod
from typing import Protocol, TypeVar, runtime_checkable

_T = TypeVar("_T")


@runtime_checkable
class SupportsSidebarWidth(Protocol[_T]):
    __slots__ = ()

    @property
    @abstractmethod
    def sidebar_width(self) -> _T: ...

    @sidebar_width.setter
    @abstractmethod
    def sidebar_width(self, value: _T) -> None: ...


@runtime_checkable
class SupportsSidebarHeight(Protocol[_T]):
    __slots__ = ()

    @property
    @abstractmethod
    def sidebar_height(self) -> _T: ...

    @sidebar_height.setter
    @abstractmethod
    def sidebar_height(self, value: _T) -> None: ...
