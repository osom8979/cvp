# -*- coding: utf-8 -*-

from abc import abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class SupportsSelected(Protocol):
    __slots__ = ()

    @property
    @abstractmethod
    def selected(self) -> bool: ...

    @selected.setter
    @abstractmethod
    def selected(self, value: bool) -> None: ...
