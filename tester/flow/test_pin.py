# -*- coding: utf-8 -*-

from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.flow.pin import FlowPin, FlowStream, FlowType


class PinTestCase(TestCase):
    def test_serializable(self):
        pin = FlowPin("test", FlowType.data, FlowStream.output, "int", "left", "#000")
        obj = serialize(pin)
        result = deserialize(obj, FlowPin)
        self.assertEqual(pin, result)

    def test_required_serializable(self):
        pin = FlowPin("test", FlowType.data, FlowStream.output)
        obj = serialize(pin)
        self.assertIsInstance(obj, dict)
        self.assertEqual("", obj.pop("dtype"))
        self.assertEqual("", obj.pop("icon"))
        self.assertEqual("", obj.pop("color"))
        result = deserialize(obj, FlowPin)
        self.assertEqual(pin, result)


if __name__ == "__main__":
    main()
