# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.flow.templates.node import FlowNode
from cvp.flow.templates.pin import FlowPin


class NodeTestCase(TestCase):
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
        obj = serialize(node)
        result = deserialize(obj, FlowNode)
        self.assertEqual(node, result)

    def test_copy(self):
        pin1 = FlowPin("A")
        node1 = FlowNode("A", class_pins=[pin1])
        node2 = copy(node1)
        self.assertEqual(node1, node2)

        node2.class_pins[0].class_name = "B"
        self.assertEqual(node1, node2)

    def test_deepcopy(self):
        pin1 = FlowPin("A")
        node1 = FlowNode("A", class_pins=[pin1])
        node2 = deepcopy(node1)
        self.assertEqual(node1, node2)

        pin2 = FlowPin("B")
        node2.class_pins[0] = pin2
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    main()
