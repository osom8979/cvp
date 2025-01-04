# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.types.colors import RGBA, WHITE_RGBA


@dataclass
class DataType:
    name: str = str()
    docs: str = str()
    icon: str = str()
    color: RGBA = WHITE_RGBA
    path: str = str()
