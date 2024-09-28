# -*- coding: utf-8 -*-

from collections import OrderedDict

from cvp.flow.catalog import FlowCatalog
from cvp.flow.graph import FlowGraph


class FlowManager:
    catalogs: OrderedDict[str, FlowCatalog]
    graphs: OrderedDict[str, FlowGraph]

    def __init__(self):
        self.catalogs = OrderedDict()
        self.graphs = OrderedDict()
