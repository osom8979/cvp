# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.types.dataclass.public_eq import public_eq


@public_eq
@dataclass
class View:
    pan_x: float = 0.0
    pan_y: float = 0.0
    zoom: float = 1.0
