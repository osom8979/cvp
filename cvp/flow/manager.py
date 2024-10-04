# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Optional

from cvp.flow.catalog import FlowCatalog
from cvp.flow.graph import FlowGraph


class FlowManager:
    graphs: OrderedDict[str, FlowGraph]
    current_graph: Optional[FlowGraph]

    def __init__(self):
        self.catalog = FlowCatalog.from_builtins()
        self.graphs = OrderedDict()
        self.current_graph = None

    def create_graphs(self, key: str) -> FlowGraph:
        if key in self.graphs:
            raise KeyError(f"Already created flow graph: '{key}'")
        graph = FlowGraph(key)
        self.graphs[key] = graph
        return graph
