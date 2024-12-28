# -*- coding: utf-8 -*-

from typing import List, NamedTuple, Union

from cvp.flow.datas.arc import Arc
from cvp.flow.datas.node import Node
from cvp.flow.datas.pin import Pin


class SelectedItems(NamedTuple):
    nodes: List[Node]
    pins: List[Pin]
    arcs: List[Arc]

    @property
    def all(self) -> List[Union[Node, Pin, Arc]]:
        return self.nodes + self.pins + self.arcs

    def __len__(self) -> int:
        return len(self.all)
