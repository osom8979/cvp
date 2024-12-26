# -*- coding: utf-8 -*-

from typing import NamedTuple

from cvp.flow.datas.node import Node
from cvp.flow.datas.pin import Pin
from cvp.flow.datas.prefix import Prefix


class NodePin(NamedTuple):
    node: Node
    pin: Pin

    def __str__(self):
        return f"{self.node.name}{Prefix.pin.value}{self.pin.name}"
