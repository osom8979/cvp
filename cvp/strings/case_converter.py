# -*- coding: utf-8 -*-

from re import Pattern
from re import compile as re_compile
from typing import Final

_CAMELCASE_TO_SNAKECASE2: Final[Pattern] = re_compile(r"([a-z0-9])([A-Z])")
_CAMELCASE_TO_SNAKECASE1: Final[Pattern] = re_compile(r"([A-Z][A-Z]+)([A-Z][a-z0-9]+)")


def camelcase_to_snakecase(name: str) -> str:
    s1 = _CAMELCASE_TO_SNAKECASE1.sub(r"\1_\2", name)
    s2 = _CAMELCASE_TO_SNAKECASE2.sub(r"\1_\2", s1)
    return s2.lower()
