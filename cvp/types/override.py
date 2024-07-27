# -*- coding: utf-8 -*-

from functools import wraps
from types import FunctionType
from typing import Callable, TypeVar, Union

_WrappedMethod = TypeVar("_WrappedMethod", bound=Union[FunctionType, Callable])
_DecoratorMethod = Callable[[_WrappedMethod], _WrappedMethod]


def _fake_override(func) -> Union[_DecoratorMethod, _WrappedMethod]:
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


try:
    from overrides import override
except ImportError:
    override = _fake_override  # type: ignore[assignment]
