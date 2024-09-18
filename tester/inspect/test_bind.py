# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.inspect.bind import force_bind


class BindTestCase(TestCase):
    def test_force_bind_empty(self):
        def _test_func():
            pass

        ba = force_bind(_test_func, 1, "2", 3.0, k1=4, k2="5", k3=6.0)
        self.assertEqual(len(ba.args), 0)
        self.assertEqual(len(ba.kwargs), 0)
        self.assertIsNone(ba())

    def test_force_bind_args_kwargs(self):
        def _test_func(*args, **kwargs):
            pass

        ba = force_bind(_test_func, 1, "2", 3.0, k1=4, k2="5", k3=6.0)
        self.assertEqual(len(ba.args), 3)
        self.assertEqual(ba.args[0], 1)
        self.assertEqual(ba.args[1], "2")
        self.assertEqual(ba.args[2], 3.0)
        self.assertEqual(len(ba.kwargs), 3)
        self.assertEqual(ba.kwargs["k1"], 4)
        self.assertEqual(ba.kwargs["k2"], "5")
        self.assertEqual(ba.kwargs["k3"], 6.0)
        self.assertIsNone(ba())

    def test_force_bind_args1(self):
        def _test_func(a):
            pass

        ba = force_bind(_test_func, 1, "2", 3.0, k1=4, k2="5", k3=6.0)
        self.assertEqual(len(ba.args), 1)
        self.assertEqual(ba.args[0], 1)
        self.assertEqual(len(ba.kwargs), 0)
        self.assertIsNone(ba())

    def test_force_bind_args1_default(self):
        def _test_func(a=999):
            pass

        ba = force_bind(_test_func)
        self.assertEqual(len(ba.args), 1)
        self.assertEqual(ba.args[0], 999)
        self.assertEqual(len(ba.kwargs), 0)
        self.assertIsNone(ba())

    def test_force_bind_args1_kwargs1(self):
        def _test_func(a, b=999):
            pass

        ba = force_bind(_test_func, b=100)
        self.assertEqual(len(ba.args), 2)
        self.assertEqual(ba.args[0], None)
        self.assertEqual(ba.args[1], 100)
        self.assertEqual(len(ba.kwargs), 0)
        self.assertIsNone(ba())

    def test_force_bind_args2(self):
        def _test_func(a, b=999, /):
            pass

        ba = force_bind(_test_func, b=100)
        self.assertEqual(len(ba.args), 2)
        self.assertEqual(ba.args[0], None)
        self.assertEqual(ba.args[1], 999)
        self.assertEqual(len(ba.kwargs), 0)
        self.assertIsNone(ba())

    def test_force_bind_kwargs2(self):
        def _test_func(*, a, b=999):
            pass

        ba = force_bind(_test_func, b=100)
        self.assertEqual(len(ba.args), 0)
        self.assertEqual(len(ba.kwargs), 2)
        self.assertEqual(ba.kwargs["a"], None)
        self.assertEqual(ba.kwargs["b"], 100)
        self.assertIsNone(ba())

    def test_force_bind_complex(self):
        def _test_func(a, b=100, /, c=200, d=300, *args, e, f=999, g, **kwargs):
            pass

        ba = force_bind(_test_func, 1, "2", 20, 30, c=3, f=4, e="5", k=80, b=14)
        self.assertEqual(len(ba.args), 5)
        self.assertEqual(ba.args[0], 1)  # a
        self.assertEqual(ba.args[1], "2")  # b
        self.assertEqual(ba.args[2], 3)  # c
        self.assertEqual(ba.args[3], 20)  # d
        self.assertEqual(ba.args[4], 30)  # *args
        self.assertEqual(len(ba.kwargs), 5)
        self.assertNotIn("c", ba.kwargs)
        self.assertEqual(ba.kwargs["e"], "5")
        self.assertEqual(ba.kwargs["f"], 4)
        self.assertEqual(ba.kwargs["g"], None)
        self.assertEqual(ba.kwargs["b"], 14)
        self.assertEqual(ba.kwargs["k"], 80)
        self.assertIsNone(ba())


if __name__ == "__main__":
    main()
