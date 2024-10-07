# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.flow.instances.pin import Pin


class PinTestCase(TestCase):
    def test_serializable(self):
        pin = Pin()
        obj = serialize(pin)
        result = deserialize(obj, Pin)
        self.assertEqual(pin, result)

    def test_copy(self):
        pin1 = Pin()
        pin2 = copy(pin1)
        self.assertEqual(pin1, pin2)

    def test_deepcopy(self):
        pin1 = Pin()
        pin2 = deepcopy(pin1)
        self.assertEqual(pin1, pin2)


if __name__ == "__main__":
    main()
