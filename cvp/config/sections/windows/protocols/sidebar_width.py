# -*- coding: utf-8 -*-

from typing import Protocol, runtime_checkable


@runtime_checkable
class SidebarWidthProtocol(Protocol):
    @property
    def sidebar_width(self) -> int: ...

    @sidebar_width.setter
    def sidebar_width(self, value: int) -> None: ...
