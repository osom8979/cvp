# -*- coding: utf-8 -*-

from typing import NamedTuple

from cvp.flow.datas import NodePin


class ConnectPair(NamedTuple):
    output: NodePin
    input: NodePin
