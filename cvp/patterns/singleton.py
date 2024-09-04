# -*- coding: utf-8 -*-

from inspect import signature
from typing import Any, Optional, Type, TypeVar, Union

_T = TypeVar("_T")


def singleton(base: type):
    class _Wrapper(base):
        __singleton_instance__ = None

        def __new__(cls, *args, **kwargs):
            if _Wrapper.__singleton_instance__ is None:
                super_cls = super(_Wrapper, cls)
                if object.__new__ == super_cls.__new__:
                    instance = object.__new__(cls)
                else:
                    new_sig = signature(super_cls.__new__)
                    ba = new_sig.bind(cls, *args, **kwargs)
                    ba.apply_defaults()
                    instance = super_cls.__new__(*ba.args, **ba.kwargs)
                _Wrapper.__singleton_instance__ = instance
                _Wrapper.__singleton_instance__.__singleton_sealed__ = False
            return _Wrapper.__singleton_instance__

        def __init__(self, *args, **kwargs):
            if self.__singleton_sealed__:
                return
            super(_Wrapper, self).__init__(*args, **kwargs)
            self.__singleton_sealed__ = True

    _Wrapper.__name__ = base.__name__
    return _Wrapper


def is_singleton(base: Union[type, Type[_T]]) -> bool:
    return hasattr(base, "__singleton_instance__")


def is_singleton_instance(base: Any) -> bool:
    if isinstance(base, type):
        return is_singleton(base)
    else:
        return is_singleton(type(base))


def get_singleton_instance(base: Type[_T]) -> Optional[_T]:
    if not is_singleton(base):
        raise TypeError(f"{base.__name__} is not a singleton type")
    return getattr(base, "__singleton_instance__", None)
