# -*- coding: utf-8 -*-

from typing import Protocol, runtime_checkable


@runtime_checkable
class SelectedProtocol(Protocol):
    @property
    def selected(self) -> bool: ...

    @selected.setter
    def selected(self, value: bool) -> None: ...
