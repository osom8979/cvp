# -*- coding: utf-8 -*-

from typing import Callable, Generic, Optional, TypeVar

_T = TypeVar("_T")


class StateWatcher(Generic[_T]):
    def __init__(
        self,
        value: _T,
        prev: _T,
        on_change: Optional[Callable[[_T, _T], None]] = None,
    ):
        self._changed = False
        self._prev = prev
        self._value = value
        self._on_change = on_change

    def __bool__(self):
        return self._changed

    @property
    def changed(self) -> bool:
        return self._changed

    @property
    def prev(self) -> _T:
        return self._prev

    @prev.setter
    def prev(self, prev: _T) -> None:
        self._prev = prev

    @property
    def value(self) -> _T:
        return self._value

    @value.setter
    def value(self, value: _T) -> None:
        self._value = value

    def update(self, value: _T, *, no_emit=False):
        self._changed = self._value != value and not no_emit
        if self._on_change is not None and self._changed:
            self._on_change(value, self._value)
        self._prev = self._value
        self._value = value
        return self
