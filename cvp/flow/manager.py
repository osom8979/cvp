# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Optional

from cvp.flow.catalog import FlowCatalog
from cvp.flow.instances.graph import Graph


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

    def add_node(self, node_path: str) -> None:
        pass
