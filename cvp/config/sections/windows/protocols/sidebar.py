# -*- coding: utf-8 -*-

from typing import Protocol, runtime_checkable


@runtime_checkable
class SidebarWidthProtocol(Protocol):
    @property
    def sidebar_width(self) -> int: ...

    @sidebar_width.setter
    def sidebar_width(self, value: int) -> None: ...


@runtime_checkable
class SidebarHeightProtocol(Protocol):
    @property
    def sidebar_height(self) -> int: ...

    @sidebar_height.setter
    def sidebar_height(self, value: int) -> None: ...
