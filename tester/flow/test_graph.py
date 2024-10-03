# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.flow.arc import FlowArc
from cvp.flow.graph import FlowGraph
from cvp.flow.node import FlowNode
from cvp.flow.pin import FlowPin


class GraphTestCase(TestCase):
    def test_serializable(self):
        pin = FlowPin(
            class_name="pin",
            class_docs="unknown1",
            class_action="data",
            class_stream="output",
            class_dtype="numpy.ndarray",
            class_required=True,
            class_icon="default",
            class_color="#000",
        )
        node = FlowNode(
            class_name="node",
            class_docs="unknown2",
            class_icon="default",
            class_color="red",
            class_pins=[pin],
        )
        arc = FlowArc(
            class_name="arc",
            class_docs="unknown3",
            class_icon="default",
            class_color="blue",
        )
        graph = FlowGraph(
            class_name="graph",
            class_docs="unknown4",
            class_icon="default",
            class_color="green",
            class_nodes=[node],
            class_arcs=[arc],
        )
        obj = serialize(graph)
        result = deserialize(obj, FlowGraph)
        self.assertEqual(graph, result)

    def test_copy(self):
        pin1 = FlowPin("A")
        node1 = FlowNode("A", class_pins=[pin1])
        arc1 = FlowArc("A")
        graph1 = FlowGraph("A", class_nodes=[node1], class_arcs=[arc1])
        graph2 = copy(graph1)
        self.assertEqual(graph1, graph2)

        graph2.class_nodes[0].class_name = "B"
        self.assertEqual(graph1, graph2)

    def test_deepcopy(self):
        pin1 = FlowPin("A")
        node1 = FlowNode("A", class_pins=[pin1])
        arc1 = FlowArc("A")
        graph1 = FlowGraph("A", class_nodes=[node1], class_arcs=[arc1])
        graph2 = deepcopy(graph1)
        self.assertEqual(graph1, graph2)

        graph2.class_nodes[0].class_name = "B"
        self.assertNotEqual(graph1, graph2)


if __name__ == "__main__":
    main()
