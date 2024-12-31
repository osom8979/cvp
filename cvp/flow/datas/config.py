# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.types.dataclass.public_eq import public_eq


@public_eq
@dataclass
class Config:
    arc_hovering_tolerance: float = 4.0
