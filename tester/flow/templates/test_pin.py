# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.flow.templates.pin import FlowPin


class PinTestCase(TestCase):
    def test_serializable(self):
        pin = FlowPin(
            class_name="test",
            class_docs="unknown",
            class_action="data",
            class_stream="output",
            class_dtype="numpy.ndarray",
            class_required=True,
            class_icon="default",
            class_color="#000",
        )
        obj = serialize(pin)
        result = deserialize(obj, FlowPin)
        self.assertEqual(pin, result)

    def test_copy(self):
        pin1 = FlowPin("A")
        pin2 = copy(pin1)
        self.assertEqual(pin1, pin2)

    def test_deepcopy(self):
        pin1 = FlowPin("A")
        pin2 = deepcopy(pin1)
        self.assertEqual(pin1, pin2)


if __name__ == "__main__":
    main()
