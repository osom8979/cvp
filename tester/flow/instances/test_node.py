# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.flow.instances.node import Node


class NodeTestCase(TestCase):
    def test_serializable(self):
        node = Node()
        obj = serialize(node)
        result = deserialize(obj, Node)
        self.assertEqual(node, result)

    def test_copy(self):
        node1 = Node()
        node2 = copy(node1)
        self.assertEqual(node1, node2)

    def test_deepcopy(self):
        node1 = Node()
        node2 = deepcopy(node1)
        self.assertEqual(node1, node2)


if __name__ == "__main__":
    main()
