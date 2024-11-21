# -*- coding: utf-8 -*-

from inspect import getmembers, isroutine, signature
from typing import Any, Callable, Dict, List, Optional

from pygame.event import Event
from pygame.event import event_name as get_event_name

from cvp.inspect.bind import force_bind
from cvp.pygame.constants.event_type import EventType
from cvp.pygame.events.attribute import get_event_type, has_event_type
from cvp.pygame.events.interface import EventInterface


class EventCallable:
    def __init__(self, func: Callable, same_signature=False):
        self._func = func
        self._same_signature = same_signature

    def __call__(self, *args, **kwargs):
        if self._same_signature:
            return self._func(*args, **kwargs)
        else:
            return force_bind(self._func, *args, **kwargs)()


class EventWrapper:
    _callbacks: List[EventCallable]

    def __init__(
        self,
        event_type: EventType,
        name: str,
        func: Callable[..., Any],
    ):
        self._params = list(signature(func).parameters.keys())
        self._event_type = event_type
        self._event_name = get_event_name(event_type)
        self._fallback_name = name
        self._fallback_func = func
        self._fallback_signature = signature(func)
        self._callbacks = list()

    def compare_fallback_kwargs(self, func: Callable) -> bool:
        left = [(p.name, p.kind) for p in self._fallback_signature.parameters.values()]
        right = [(p.name, p.kind) for p in signature(func).parameters.values()]
        return left == right

    def __call__(self, event: Optional[Event] = None) -> bool:
        kwargs = {p: event.dict[p] for p in self._params} if event else dict()

        for callback in self._callbacks:
            if bool(callback(**kwargs)):
                return True

        return bool(self._fallback_func(**kwargs))

    def append_callback(self, func: Callable) -> None:
        self._callbacks.append(EventCallable(func, self.compare_fallback_kwargs(func)))

    def clear_callback(self) -> None:
        self._callbacks.clear()


def create_event_map(obj: Any, cls=EventInterface) -> Dict[int, EventWrapper]:
    result = dict()
    event_interfaces = dict(getmembers(cls))
    event_attributes = getmembers(obj, lambda a: isroutine(a))

    for key, func in event_attributes:
        event_interface = event_interfaces.get(key)
        if event_interface is None:
            continue
        if not has_event_type(event_interface):
            continue
        event_type = get_event_type(event_interface)
        assert isinstance(event_type, int)
        result[event_type] = EventWrapper(EventType(event_type), key, func)

    return result
