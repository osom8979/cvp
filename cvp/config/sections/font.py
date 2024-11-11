# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

from cvp.config.sections.bases.manager import ManagerWindowConfig


@dataclass
class FontConfig:
    family: str = field(default_factory=str)
    scale: float = 1.0
    pixels: int = 14


@dataclass
class FontManagerConfig(ManagerWindowConfig):
    pass
