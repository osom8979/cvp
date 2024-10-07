# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.flow.instances.graph import Graph


class GraphTestCase(TestCase):
    def test_serializable(self):
        graph = Graph()
        obj = serialize(graph)
        result = deserialize(obj, Graph)
        self.assertEqual(graph, result)

    def test_copy(self):
        graph1 = Graph()
        graph2 = copy(graph1)
        self.assertEqual(graph1, graph2)

    def test_deepcopy(self):
        graph1 = Graph()
        graph2 = deepcopy(graph1)
        self.assertEqual(graph1, graph2)


if __name__ == "__main__":
    main()
