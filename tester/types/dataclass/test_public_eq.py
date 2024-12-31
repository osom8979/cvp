# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List
from unittest import TestCase, main

from cvp.types.dataclass.public_eq import public_eq
from cvp.types.shapes import Point


@public_eq
@dataclass
class _Val:
    value0: List[Point] = field(default_factory=list)
    value1: Dict[int, int] = field(default_factory=dict)

    _private_value: int = 0


@public_eq
@dataclass
class _Test:
    value0 = 0
    value1: int = 1
    value2: str = "2"
    value3: Point = 3, 3
    value4: _Val = field(default_factory=_Val)

    _private_value: int = 0


class PublicEqTestCase(TestCase):
    def test_equal(self):
        aa = _Val(value0=[(1, 1), (2, 2)], value1={1: 1}, _private_value=1)
        bb = _Val(value0=[(1, 1), (2, 2)], value1={1: 1}, _private_value=2)
        a = _Test(value1=10, value2="20", value3=(30, 30), value4=aa, _private_value=3)
        b = _Test(value1=10, value2="20", value3=(30, 30), value4=bb, _private_value=4)

        self.assertEqual(aa, bb)
        self.assertEqual(a, b)

        self.assertNotEqual(aa, b)
        self.assertNotEqual(a, bb)
        self.assertNotEqual(bb, a)
        self.assertNotEqual(b, aa)

    def test_list(self):
        aa = _Val(value0=[(2, 2), (1, 1)])
        bb = _Val(value0=[(1, 1), (2, 2)])
        a = _Test(value4=aa)
        b = _Test(value4=bb)

        self.assertNotEqual(aa, bb)
        self.assertNotEqual(a, b)

        self.assertNotEqual(aa, b)
        self.assertNotEqual(a, bb)
        self.assertNotEqual(bb, a)
        self.assertNotEqual(b, aa)


if __name__ == "__main__":
    main()
