# -*- coding: utf-8 -*-

from typing import Optional

from cvp.flow.datas.graph import Graph


class FlowCursor:
    def __init__(self, graph: Optional[Graph] = None):
        self._graph = graph

    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self, value: Optional[Graph]) -> None:
        self._graph = value
