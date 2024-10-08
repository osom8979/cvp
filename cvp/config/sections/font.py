# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class FontConfig:
    family: str = ""
    scale: float = 1.0
    pixels: int = 14
