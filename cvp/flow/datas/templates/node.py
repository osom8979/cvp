# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List

from cvp.flow.datas.templates.pin import PinTemplate
from cvp.types.colors import RGBA, WHITE_RGBA


@dataclass
class NodeTemplate:
    name: str = str()
    docs: str = str()
    emblem: str = str()
    color: RGBA = WHITE_RGBA
    pins: List[PinTemplate] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
