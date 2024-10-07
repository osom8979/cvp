# -*- coding: utf-8 -*-

from typing import Final, Optional

EVENT_TYPE_ATTR_NAME: Final[str] = "__event_type__"


def has_event_type(func) -> bool:
    return hasattr(func, EVENT_TYPE_ATTR_NAME)


def get_event_type(func) -> Optional[int]:
    return getattr(func, EVENT_TYPE_ATTR_NAME, None)


def set_event_type(func, event_type: int) -> None:
    setattr(func, EVENT_TYPE_ATTR_NAME, event_type)
