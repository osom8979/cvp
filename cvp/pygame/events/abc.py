# -*- coding: utf-8 -*-

from abc import abstractmethod
from functools import wraps

from cvp.pygame.events.attribute import set_event_type


def abstractevent(event_type: int):
    def _param_wrapper(func):
        abstractmethod(func)
        set_event_type(func, event_type)

        @wraps(func)
        def _func_wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return _func_wrapper

    return _param_wrapper
