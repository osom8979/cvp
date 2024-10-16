# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.patterns.proxies.pod import Boolean, Floating, Integer


class PodTestCase(TestCase):
    def test_boolean(self):
        value0 = Boolean(False)
        value1 = Boolean(True)

        self.assertFalse(value0)
        self.assertTrue(value1)

        self.assertNotEquals(value0, value1)
        self.assertEquals(value0, False)
        self.assertEquals(value1, True)

    def test_integer(self):
        value0 = Integer(0)
        value1 = Integer(20)

        self.assertFalse(value0)
        self.assertTrue(value1)

        self.assertNotEquals(value0, value1)
        self.assertEquals(value0, 0)
        self.assertEquals(value1, 20)

    def test_floating(self):
        value0 = Floating(0)
        value1 = Floating(20)

        self.assertFalse(value0)
        self.assertTrue(value1)

        self.assertNotEquals(value0, value1)
        self.assertEquals(value0, 0.0)
        self.assertEquals(value1, 20.0)


if __name__ == "__main__":
    main()
