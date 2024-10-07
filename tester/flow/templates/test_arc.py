# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.flow.templates.arc import FlowArc


class ArcTestCase(TestCase):
    def test_serializable(self):
        arc = FlowArc(
            class_name="test",
            class_docs="unknown",
            class_icon="default",
            class_color="#000",
        )
        obj = serialize(arc)
        result = deserialize(obj, FlowArc)
        self.assertEqual(arc, result)

    def test_copy(self):
        pin1 = FlowArc("A")
        pin2 = copy(pin1)
        self.assertEqual(pin1, pin2)

    def test_deepcopy(self):
        pin1 = FlowArc("A")
        pin2 = deepcopy(pin1)
        self.assertEqual(pin1, pin2)


if __name__ == "__main__":
    main()
