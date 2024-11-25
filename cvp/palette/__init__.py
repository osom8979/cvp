# -*- coding: utf-8 -*-

from functools import lru_cache, reduce
from importlib import import_module
from types import ModuleType
from typing import Dict, List

from cvp.types.colors import RGB


def _palette_filter(module: ModuleType, key: str) -> bool:
    if not key.isupper():
        return False

    value = getattr(module, key)
    if not isinstance(value, tuple):
        return False

    if len(value) != 3:
        return False

    if not isinstance(value[0], float):
        return False
    if not isinstance(value[1], float):
        return False
    if not isinstance(value[2], float):
        return False

    assert 0 <= value[0] <= 1.0
    assert 0 <= value[1] <= 1.0
    assert 0 <= value[2] <= 1.0
    return True


def _load_palette_from_module(module: ModuleType) -> Dict[str, RGB]:
    keys = list(filter(lambda x: _palette_filter(module, x), dir(module)))
    return {k: getattr(module, k) for k in keys}


@lru_cache
def _module_suffix() -> str:
    return "" if __name__ == "__main__" else __name__ + "."


def _load_palette_from_module_name(module_name: str):
    module = import_module(_module_suffix() + module_name)
    return _load_palette_from_module(module)


@lru_cache
def basic_palette():
    return _load_palette_from_module_name("basic")


@lru_cache
def css4_palette():
    return _load_palette_from_module_name("css4")


@lru_cache
def extended_palette():
    return _load_palette_from_module_name("extended")


@lru_cache
def flat_palette():
    return _load_palette_from_module_name("flat")


@lru_cache
def tableau_palette():
    return _load_palette_from_module_name("tableau")


@lru_cache
def xkcd_palette():
    return _load_palette_from_module_name("xkcd")


@lru_cache
def global_palette_map() -> Dict[str, Dict[str, RGB]]:
    result = dict()
    result["basic"] = basic_palette()
    result["css4"] = css4_palette()
    result["extended"] = extended_palette()
    result["flat"] = flat_palette()
    result["tableau"] = tableau_palette()
    result["xkcd"] = xkcd_palette()
    return result


@lru_cache
def registered_palette_keys() -> List[str]:
    return list(global_palette_map().keys())


@lru_cache
def registered_color_count() -> int:
    return reduce(lambda x, y: x + len(y), global_palette_map().values(), 0)
