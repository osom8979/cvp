# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class Config:
    arc_hovering_tolerance: float = 4.0
