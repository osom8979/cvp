# -*- coding: utf-8 -*-

from typing import NamedTuple

from cvp.flow.datas.node import Node
from cvp.flow.datas.pin import Pin


class NodePin(NamedTuple):
    node: Node
    pin: Pin

    def __str__(self):
        return f"{self.node.name}.{self.pin.name}"
