# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.flow.datas.constants import EMPTY_TEXT, WHITE_RGBA
from cvp.types.colors import RGBA
from cvp.types.dataclass.public_eq import public_eq


@public_eq
@dataclass
class DataType:
    name: str = EMPTY_TEXT
    docs: str = EMPTY_TEXT
    icon: str = EMPTY_TEXT
    color: RGBA = WHITE_RGBA
    path: str = EMPTY_TEXT
