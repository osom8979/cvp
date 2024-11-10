# -*- coding: utf-8 -*-

from contextlib import contextmanager
from os import environ
from typing import Dict, Optional, TypeVar, Union, overload

from cvp.types.string.to_boolean import string_to_boolean

DefaultT = TypeVar("DefaultT", str, bool, int, float)


# fmt: off
@overload
def get_typed_environ_value(key: str) -> Optional[str]: ...
@overload
def get_typed_environ_value(key: str, default: str) -> str: ...
@overload
def get_typed_environ_value(key: str, default: bool) -> bool: ...
@overload
def get_typed_environ_value(key: str, default: int) -> int: ...
@overload
def get_typed_environ_value(key: str, default: float) -> float: ...
# fmt: on


def get_typed_environ_value(
    key: str,
    default: Optional[DefaultT] = None,
) -> Optional[Union[str, bool, int, float]]:
    if default is None:
        return environ.get(key)

    value = environ.get(key, str(default))
    if isinstance(default, str):
        return value
    elif isinstance(default, bool):
        return string_to_boolean(value)
    elif isinstance(default, int):
        return int(value)
    elif isinstance(default, float):
        return float(value)
    else:
        raise TypeError(f"Unsupported default type: {type(default).__name__}")


def environ_dict() -> Dict[str, str]:
    return {k: str(environ.get(k)) for k in environ if environ}


def exchange_env(key: str, exchange: Optional[str]) -> Optional[str]:
    result = environ.get(key)
    if result is not None:
        environ.pop(key)
    if exchange is not None:
        environ[key] = exchange
    return result


@contextmanager
def exchange_env_context(key: str, exchange: Optional[str]):
    original = exchange_env(key, exchange)
    try:
        yield
    finally:
        exchange_env(key, original)
