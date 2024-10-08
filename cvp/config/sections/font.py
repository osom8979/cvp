# -*- coding: utf-8 -*-

from dataclasses import dataclass, field


@dataclass
class FontConfig:
    family: str = field(default_factory=str)
    scale: float = 1.0
    pixels: int = 14
