# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List

from cvp.flow.datas.constants import EMPTY_TEXT, WHITE_RGBA
from cvp.flow.datas.templates.pin import PinTemplate
from cvp.types.colors import RGBA


@dataclass
class NodeTemplate:
    name: str = EMPTY_TEXT
    docs: str = EMPTY_TEXT
    emblem: str = EMPTY_TEXT
    color: RGBA = WHITE_RGBA
    pins: List[PinTemplate] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
