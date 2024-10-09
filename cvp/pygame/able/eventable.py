# -*- coding: utf-8 -*-

from typing import Optional, Sequence, Union

from pygame import event as pg_event
from pygame.event import Event

from cvp.pygame.types import SequenceProtocol


class Eventable:
    @staticmethod
    def event_pump():
        return pg_event.pump()

    @staticmethod
    def event_get(
        event_type: Optional[Union[int, Sequence[int]]] = None,
        pump=True,
        exclude: Optional[Union[int, Sequence[int]]] = None,
    ):
        assert isinstance(event_type, (type(None), int, SequenceProtocol))
        assert isinstance(exclude, (type(None), int, SequenceProtocol))
        return pg_event.get(event_type, pump, exclude)

    @staticmethod
    def event_poll():
        return pg_event.poll()

    @staticmethod
    def event_wait(timeout=0):
        return pg_event.wait(timeout)

    @staticmethod
    def event_peek(event_type: Optional[Union[int, Sequence[int]]] = None, pump=True):
        assert isinstance(event_type, (type(None), int, SequenceProtocol))
        return pg_event.peek(event_type, pump)

    @staticmethod
    def event_clear(event_type: Optional[Union[int, Sequence[int]]] = None):
        assert isinstance(event_type, (type(None), int, SequenceProtocol))
        return pg_event.clear(event_type)

    @staticmethod
    def event_name(event_type: int):
        return pg_event.event_name(event_type)

    @staticmethod
    def event_set_blocked(event_type: Optional[Union[int, Sequence[int]]] = None):
        assert isinstance(event_type, (type(None), int, SequenceProtocol))
        return pg_event.set_blocked(event_type)

    @staticmethod
    def event_set_allowed(event_type: Optional[Union[int, Sequence[int]]] = None):
        assert isinstance(event_type, (type(None), int, SequenceProtocol))
        return pg_event.set_allowed(event_type)

    @staticmethod
    def event_get_blocked(event_type: Union[int, Sequence[int]]):
        assert isinstance(event_type, (int, SequenceProtocol))
        return pg_event.get_blocked(event_type)

    @staticmethod
    def event_set_grab(grab: bool):
        return pg_event.set_grab(grab)

    @staticmethod
    def event_get_grab():
        return pg_event.get_grab()

    @staticmethod
    def event_post(event: Event):
        return pg_event.post(event)

    @staticmethod
    def event_custom_type():
        return pg_event.custom_type()
