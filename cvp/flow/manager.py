# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Optional, Union

from cvp.flow.catalog import FlowCatalog
from cvp.flow.datas import Graph, Node, Pin
from cvp.flow.path import FlowPath


class FlowManager:
    def __init__(self, *, cursor: Optional[str] = None):
        self._catalog = FlowCatalog.from_builtins()
        self._graphs = OrderedDict[str, Graph]()
        self._cursor = cursor

    @property
    def catalog(self):
        return self._catalog

    @property
    def cursored(self):
        return bool(self._cursor)

    @property
    def current_graph(self) -> Optional[Graph]:
        if self._cursor is None:
            return None
        return self._graphs.get(self._cursor, None)

    def select_graph(self, key: str) -> None:
        if key not in self._graphs:
            raise KeyError(f"Not exists flow graph: '{key}'")
        self._cursor = key

    def deselect_graph(self) -> None:
        self._cursor = None

    def create_graph(
        self,
        key: str,
        *,
        template: Optional[str] = None,
        select=False,
    ) -> Graph:
        if key in self._graphs:
            raise KeyError(f"Already created flow graph: '{key}'")
        template = template if template else str()
        assert isinstance(template, str)
        graph = Graph(name=key)
        self._graphs[key] = graph
        if select:
            self._cursor = key
        return graph

    def remove_graph(self, key: str) -> Graph:
        if key == self._cursor:
            raise KeyError(f"The selected graph cannot be removed: '{key}'")
        if key in self._graphs:
            raise KeyError(f"Not exists flow graph: '{key}'")
        return self._graphs.pop(key)

    def get_node_template(self, path: Union[str, FlowPath]):
        return self._catalog.get_node_template(path)

    def add_node(self, path: Union[str, FlowPath]) -> None:
        graph = self.current_graph
        if graph is None:
            raise LookupError("A graph must be selected")

        node_template = self.get_node_template(path)
        node_name = node_template.name
        node_docs = node_template.docs
        node_icon = node_template.icon
        node_color = node_template.color
        node_pins = list()
        for pin_template in node_template.pins:
            pin = Pin(
                name=pin_template.name,
                docs=pin_template.docs,
                dtype=pin_template.dtype,
                action=pin_template.action,
                stream=pin_template.stream,
                required=pin_template.required,
            )
            node_pins.append(pin)

        node = Node(
            name=node_name,
            docs=node_docs,
            icon=node_icon,
            color=node_color,
            pins=node_pins,
        )
        graph.nodes.append(node)
