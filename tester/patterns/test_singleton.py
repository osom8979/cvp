# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.patterns.singleton import get_singleton_instance, is_singleton, singleton


class _NoSingleton:
    pass


@singleton
class _NoInstanceSingleton:
    pass


@singleton
class _TestNoInheritance:
    def __init__(self, value=999):
        self.value = value

    @classmethod
    def name(cls):
        return cls.__name__


class _TestBase:
    def __new__(cls, value=888):
        return object.__new__(cls)

    def __init__(self, value=999):
        self.value = value

    @classmethod
    def name(cls):
        return cls.__name__


@singleton
class _TestInheritance(_TestBase):
    def __init__(self, value=999):
        super().__init__(value)

    @classmethod
    def name(cls):
        return cls.__name__


class SingletonTestCase(TestCase):
    def test_no_inheritance(self):
        self.assertIsNone(get_singleton_instance(_TestNoInheritance))

        o0 = _TestNoInheritance(100)
        o1 = _TestNoInheritance(200)
        o2 = _TestNoInheritance(300)
        o3 = _TestNoInheritance()
        o4 = get_singleton_instance(_TestNoInheritance)

        self.assertTrue(hasattr(o0, "__singleton_instance__"))
        self.assertTrue(hasattr(o1, "__singleton_instance__"))
        self.assertTrue(hasattr(o2, "__singleton_instance__"))
        self.assertTrue(hasattr(o3, "__singleton_instance__"))
        self.assertTrue(hasattr(o4, "__singleton_instance__"))

        self.assertIsNotNone(getattr(o0, "__singleton_instance__"))
        self.assertIsNotNone(getattr(o1, "__singleton_instance__"))
        self.assertIsNotNone(getattr(o2, "__singleton_instance__"))
        self.assertIsNotNone(getattr(o3, "__singleton_instance__"))
        self.assertIsNotNone(getattr(o4, "__singleton_instance__"))

        self.assertTrue(hasattr(o0, "__singleton_sealed__"))
        self.assertTrue(hasattr(o1, "__singleton_sealed__"))
        self.assertTrue(hasattr(o2, "__singleton_sealed__"))
        self.assertTrue(hasattr(o3, "__singleton_sealed__"))
        self.assertTrue(hasattr(o4, "__singleton_sealed__"))

        self.assertEqual(o0.value, 100)
        self.assertEqual(o1.value, 100)
        self.assertEqual(o2.value, 100)
        self.assertEqual(o3.value, 100)
        self.assertEqual(o4.value, 100)

        self.assertEqual(o0.name(), "_TestNoInheritance")
        self.assertEqual(o1.name(), "_TestNoInheritance")
        self.assertEqual(o2.name(), "_TestNoInheritance")
        self.assertEqual(o3.name(), "_TestNoInheritance")
        self.assertEqual(o4.name(), "_TestNoInheritance")

        self.assertEqual(id(o0), id(o1))
        self.assertEqual(id(o0), id(o2))
        self.assertEqual(id(o0), id(o3))
        self.assertEqual(id(o0), id(o4))

    def test_is_singleton(self):
        self.assertFalse(is_singleton(_NoSingleton))
        self.assertTrue(is_singleton(_NoInstanceSingleton))
        self.assertTrue(is_singleton(_TestNoInheritance))
        self.assertFalse(is_singleton(_TestBase))
        self.assertTrue(is_singleton(_TestInheritance))

    def test_get_singleton_instance_error(self):
        with self.assertRaises(TypeError):
            get_singleton_instance(_NoSingleton)

        self.assertIsNone(get_singleton_instance(_NoInstanceSingleton))

        with self.assertRaises(TypeError):
            get_singleton_instance(_TestBase)

    def test_inheritance(self):
        self.assertIsNone(get_singleton_instance(_TestInheritance))

        o0 = _TestInheritance(100)
        o1 = _TestInheritance(200)
        o2 = _TestInheritance(300)
        o3 = _TestInheritance()
        o4 = get_singleton_instance(_TestInheritance)

        self.assertTrue(hasattr(o0, "__singleton_instance__"))
        self.assertTrue(hasattr(o1, "__singleton_instance__"))
        self.assertTrue(hasattr(o2, "__singleton_instance__"))
        self.assertTrue(hasattr(o3, "__singleton_instance__"))
        self.assertTrue(hasattr(o4, "__singleton_instance__"))

        self.assertIsNotNone(getattr(o0, "__singleton_instance__"))
        self.assertIsNotNone(getattr(o1, "__singleton_instance__"))
        self.assertIsNotNone(getattr(o2, "__singleton_instance__"))
        self.assertIsNotNone(getattr(o3, "__singleton_instance__"))
        self.assertIsNotNone(getattr(o4, "__singleton_instance__"))

        self.assertTrue(hasattr(o0, "__singleton_sealed__"))
        self.assertTrue(hasattr(o1, "__singleton_sealed__"))
        self.assertTrue(hasattr(o2, "__singleton_sealed__"))
        self.assertTrue(hasattr(o3, "__singleton_sealed__"))
        self.assertTrue(hasattr(o4, "__singleton_sealed__"))

        self.assertEqual(o0.value, 100)
        self.assertEqual(o1.value, 100)
        self.assertEqual(o2.value, 100)
        self.assertEqual(o3.value, 100)
        self.assertEqual(o4.value, 100)

        self.assertEqual(o0.name(), "_TestInheritance")
        self.assertEqual(o1.name(), "_TestInheritance")
        self.assertEqual(o2.name(), "_TestInheritance")
        self.assertEqual(o3.name(), "_TestInheritance")
        self.assertEqual(o4.name(), "_TestInheritance")

        self.assertEqual(id(o0), id(o1))
        self.assertEqual(id(o0), id(o2))
        self.assertEqual(id(o0), id(o3))
        self.assertEqual(id(o0), id(o4))


if __name__ == "__main__":
    main()
