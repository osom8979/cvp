# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List

from cvp.flow.datas.constants import EMPTY_TEXT, WHITE_RGBA
from cvp.flow.datas.dtype import DataType
from cvp.flow.datas.templates.arc import ArcTemplate
from cvp.flow.datas.templates.node import NodeTemplate
from cvp.types.colors import RGBA


@dataclass
class GraphTemplate:
    name: str = EMPTY_TEXT
    docs: str = EMPTY_TEXT
    icon: str = EMPTY_TEXT
    color: RGBA = WHITE_RGBA
    nodes: List[NodeTemplate] = field(default_factory=list)
    arcs: List[ArcTemplate] = field(default_factory=list)
    dtypes: List[DataType] = field(default_factory=list)
