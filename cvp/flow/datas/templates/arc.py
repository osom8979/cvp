# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.flow.datas.constants import EMPTY_TEXT
from cvp.types.dataclass.public_eq import public_eq


@public_eq
@dataclass
class ArcTemplate:
    output_node: str = EMPTY_TEXT
    output_pin: str = EMPTY_TEXT
    input_node: str = EMPTY_TEXT
    input_pin: str = EMPTY_TEXT
