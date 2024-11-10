# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Callable, Generic, Optional, final

from cvp.patterns.proxy import ValueProxy, ValueT
from cvp.types.override import override


class StateObserverInterface(Generic[ValueT], ABC):
    @abstractmethod
    def on_update(self, value: ValueT, prev: ValueT) -> Optional[bool]:
        raise NotImplementedError

    @abstractmethod
    def update(self) -> bool:
        raise NotImplementedError


class StateObserver(StateObserverInterface[ValueT]):
    def __init__(
        self,
        proxy: ValueProxy[ValueT],
        callback: Optional[Callable[[ValueT, ValueT], Optional[bool]]] = None,
    ) -> None:
        self._proxy = proxy
        self._callback = callback
        self._prev_value = proxy.get()

    @property
    def proxy(self):
        return self._proxy

    @property
    def prev_value(self):
        return self._prev_value

    @override
    def on_update(self, value: ValueT, prev: ValueT) -> Optional[bool]:
        if self._callback is not None:
            return self._callback(value, prev)
        else:
            return False

    @override
    def update(self) -> bool:
        next_value = self._proxy.get()
        if self._prev_value == next_value:
            return False

        try:
            return bool(self.on_update(next_value, self._prev_value))
        finally:
            self._prev_value = next_value


@final
class OneShotStateObserver(StateObserver[ValueT]):
    @override
    def on_update(self, value: ValueT, prev: ValueT) -> Optional[bool]:
        assert self._callback is not None
        self._callback(value, prev)
        return True


class StateWatcher:
    def __init__(self, *observers: StateObserverInterface) -> None:
        self._observers = set(observers)

    def __bool__(self):
        return bool(self._observers)

    def __len__(self):
        return self._observers.__len__()

    def __iter__(self):
        return self._observers.__iter__()

    def register(self, observer: StateObserverInterface) -> None:
        self._observers.add(observer)

    def oneshot(
        self,
        proxy: ValueProxy[ValueT],
        callback: Callable[[ValueT, ValueT], None],
    ) -> None:
        self.register(OneShotStateObserver(proxy, callback))

    def unregister(self, observer: StateObserverInterface) -> None:
        self._observers.remove(observer)

    def update(self):
        consumed_observers = list()
        for observer in self._observers:
            if observer.update():
                consumed_observers.append(observer)
        for observer in consumed_observers:
            self._observers.remove(observer)
        return consumed_observers
