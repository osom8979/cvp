# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.flow.instances.arc import Arc


class ArcTestCase(TestCase):
    def test_serializable(self):
        arc = Arc()
        obj = serialize(arc)
        result = deserialize(obj, Arc)
        self.assertEqual(arc, result)

    def test_copy(self):
        arc1 = Arc()
        arc2 = copy(arc1)
        self.assertEqual(arc1, arc2)

    def test_deepcopy(self):
        arc1 = Arc()
        arc2 = deepcopy(arc1)
        self.assertEqual(arc1, arc2)


if __name__ == "__main__":
    main()
