# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class ArcTemplate:
    output_node: str = str()
    output_pin: str = str()
    input_node: str = str()
    input_pin: str = str()
