# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Optional

from cvp.flow.catalog import FlowCatalog
from cvp.flow.instances.graph import Graph
from cvp.flow.path import FlowPath


class FlowManager:
    def __init__(self):
        self._catalog = FlowCatalog.from_builtins()
        self._graphs = OrderedDict[str, Graph]()
        self._cursor = str()

    @property
    def catalog(self):
        return self._catalog

    @property
    def current(self) -> Optional[Graph]:
        return self._graphs.get(self._cursor)

    def keys(self):
        return self._graphs.keys()

    def values(self):
        return self._graphs.values()

    def items(self):
        return self._graphs.items()

    def select(self, key: str) -> None:
        if key not in self._graphs:
            raise KeyError(f"Not exists flow graph: '{key}'")
        self._cursor = key

    def deselect(self) -> None:
        self._cursor = str()

    def create_graphs(self, key: str, select=False) -> Graph:
        if key in self._graphs:
            raise KeyError(f"Already created flow graph: '{key}'")
        graph = Graph(key)
        self._graphs[key] = graph
        if select:
            self._cursor = key
        return graph

    def get_node(self, module_path: str, node_name: str):
        return self._catalog[module_path][node_name]

    def get_node_with_flow_path(self, flow_path: FlowPath):
        module, node = flow_path.split()
        return self.get_node(module, node)

    def get_node_with_path(self, node_path: str):
        return self.get_node_with_flow_path(FlowPath(node_path))

    def add_node(self, node_path: str) -> None:
        node = self.get_node_with_path(node_path)
        if not self.current:
            raise ValueError("Not exists flow graph")
        self.current.add_node(node)
