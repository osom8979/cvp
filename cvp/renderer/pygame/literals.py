# -*- coding: utf-8 -*-

from typing import Literal

ViewKind = Literal[
    "0",
    "1",
    "2",
    "3",
    b"0",
    b"1",
    b"2",
    b"3",
    "r",
    "g",
    "b",
    "a",
    "R",
    "G",
    "B",
    "A",
    b"r",
    b"g",
    b"b",
    b"a",
    b"R",
    b"G",
    b"B",
    b"A",
]

FromStringFormat = Literal[
    "P",
    "RGB",
    "RGBX",
    "RGBA",
    "ARGB",
    "BGRA",
]

ToStringFormat = Literal[
    FromStringFormat,
    "RGBA_PREMULT",
    "ARGB_PREMULT",
]
