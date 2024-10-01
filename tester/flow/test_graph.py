# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.flow.graph import FlowGraph, get_serialized_hints


class GraphTestCase(TestCase):
    def test_hints(self):
        hints = get_serialized_hints()
        self.assertEqual(str, hints.pop("name"))
        self.assertEqual(str, hints.pop("description"))
        self.assertFalse(bool(hints))

    def test_serializable(self):
        graph = FlowGraph("test", "desc")
        obj = serialize(graph)
        result = deserialize(obj, FlowGraph)
        self.assertEqual(graph, result)

    def test_required_serializable(self):
        graph = FlowGraph("test")
        obj = serialize(graph)
        self.assertIsInstance(obj, dict)
        self.assertEqual("", obj.pop("description"))
        result = deserialize(obj, FlowGraph)
        self.assertEqual(graph, result)

    def test_copy(self):
        graph1 = FlowGraph("test")
        graph2 = copy(graph1)
        self.assertNotEqual(id(graph2), id(graph1))
        self.assertEqual(graph2, graph1)

        # TODO: instance test

        graph2.description = "desc2"
        self.assertNotEqual(graph2, graph1)

    def test_deepcopy(self):
        graph1 = FlowGraph("test")
        graph2 = deepcopy(graph1)
        self.assertNotEqual(id(graph2), id(graph1))
        self.assertEqual(graph2, graph1)

        graph2.description = "desc2"
        self.assertNotEqual(graph2, graph1)


if __name__ == "__main__":
    main()
