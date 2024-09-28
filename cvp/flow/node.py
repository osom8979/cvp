# -*- coding: utf-8 -*-

from collections import OrderedDict

from cvp.flow.pin import FlowPin


class FlowNode:
    pins: OrderedDict[str, FlowPin]

    def __init__(self):
        self.pins = OrderedDict()
