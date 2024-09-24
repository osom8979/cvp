# -*- coding: utf-8 -*-

from typing import Protocol, runtime_checkable


@runtime_checkable
class CuttingEdgeProtocol(Protocol):
    @property
    def split_left(self) -> int: ...

    @split_left.setter
    def split_left(self, value: int) -> None: ...

    @property
    def split_right(self) -> int: ...

    @split_right.setter
    def split_right(self, value: int) -> None: ...

    @property
    def split_bottom(self) -> int: ...

    @split_bottom.setter
    def split_bottom(self, value: int) -> None: ...
