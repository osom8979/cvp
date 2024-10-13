# -*- coding: utf-8 -*-

from contextlib import contextmanager
from typing import Union

import imgui


@contextmanager
def indent(width: Union[int, float]):
    imgui.indent(width)
    try:
        yield
    finally:
        imgui.unindent(width)
