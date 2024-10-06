# -*- coding: utf-8 -*-
from typing import Any

from overrides import override

from cvp.flow.arc import FlowArc
from cvp.flow.builders.arc import FlowArcBuilder
from cvp.flow.builders.node import FlowNodeBuilder
from cvp.flow.graph import FlowGraphKeys
from cvp.flow.node import FlowNode


class _FlowNodeBuilderProxy(FlowNodeBuilder):
    def __init__(self, parent: "FlowGraphBuilder", **kwargs: Any):
        super().__init__(**kwargs)
        self._parent = parent

    @override
    def node_done(self):
        nodes = self._parent.kwargs[FlowGraphKeys.class_nodes]
        assert isinstance(nodes, list)

        try:
            nodes.append(FlowNode(**self.kwargs))
            return self._parent
        finally:
            self.kwargs.clear()


class _FlowArcBuilderProxy(FlowArcBuilder):
    def __init__(self, parent: "FlowGraphBuilder", **kwargs: Any):
        super().__init__(**kwargs)
        self._parent = parent

    @override
    def arc_done(self):
        arcs = self._parent.kwargs[FlowGraphKeys.class_arcs]
        assert isinstance(arcs, list)

        try:
            arcs.append(FlowArc(**self.kwargs))
            return self._parent
        finally:
            self.kwargs.clear()


class FlowGraphBuilder:
    def __init__(self, **kwargs: Any):
        self.kwargs = kwargs

        if FlowGraphKeys.class_nodes not in self.kwargs:
            self.kwargs[FlowGraphKeys.class_nodes] = list()
        if FlowGraphKeys.class_arcs not in self.kwargs:
            self.kwargs[FlowGraphKeys.class_arcs] = list()

        assert isinstance(self.kwargs[FlowGraphKeys.class_nodes], list)
        assert isinstance(self.kwargs[FlowGraphKeys.class_arcs], list)

    def graph_clear(self):
        self.kwargs.clear()
        self.kwargs[FlowGraphKeys.class_nodes] = list()
        self.kwargs[FlowGraphKeys.class_arcs] = list()

    def graph_done(self):
        try:
            return FlowNode(**self.kwargs)
        finally:
            self.kwargs.clear()

    def graph_name(self, value: str):
        self.kwargs[FlowGraphKeys.class_name] = value
        return self

    def graph_docs(self, value: str):
        self.kwargs[FlowGraphKeys.class_docs] = value
        return self

    def graph_icon(self, value: str):
        self.kwargs[FlowGraphKeys.class_icon] = value
        return self

    def graph_color(self, value: str):
        self.kwargs[FlowGraphKeys.class_color] = value
        return self

    def graph_create_node(self, **kwargs: Any):
        assert FlowGraphKeys.class_nodes in self.kwargs
        return _FlowNodeBuilderProxy(self, **kwargs)

    def graph_create_arc(self, **kwargs: Any):
        assert FlowGraphKeys.class_arcs in self.kwargs
        return _FlowArcBuilderProxy(self, **kwargs)
