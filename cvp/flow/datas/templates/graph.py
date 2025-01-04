# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List

from cvp.flow.datas.dtype import DataType
from cvp.flow.datas.templates.arc import ArcTemplate
from cvp.flow.datas.templates.node import NodeTemplate
from cvp.types.colors import RGBA, WHITE_RGBA


@dataclass
class GraphTemplate:
    name: str = str()
    docs: str = str()
    icon: str = str()
    color: RGBA = WHITE_RGBA
    nodes: List[NodeTemplate] = field(default_factory=list)
    arcs: List[ArcTemplate] = field(default_factory=list)
    dtypes: List[DataType] = field(default_factory=list)
