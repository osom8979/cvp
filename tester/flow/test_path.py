# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.flow.path import FlowPath


class PathTestCase(TestCase):
    def test_normalize(self):
        path1 = FlowPath("a.b.c.d.")
        self.assertEqual("a.b.c.d", path1.normalize())

        path2 = FlowPath("a.b.c.d.......")
        self.assertEqual("a.b.c.d", path2.normalize())

    def test_split(self):
        path1 = FlowPath("a.b.c.d")
        self.assertEqual("a.b.c", path1.get_module())
        self.assertEqual("d", path1.get_node())

        path2 = FlowPath("a")
        with self.assertRaises(IndexError):
            path2.split()

        path3 = FlowPath("a.")
        self.assertTupleEqual(("a", ""), path3.split())

        path4 = FlowPath(".a")
        self.assertTupleEqual(("", "a"), path4.split())

    def test_join(self):
        path = FlowPath("a.b.c.")
        path2 = path.join("key")
        self.assertEqual("a.b.c.key", path2)

    def test_set(self):
        paths = {FlowPath("a.b.c"), "a.b.c"}
        self.assertEqual(1, len(paths))
        path1 = paths.pop()
        self.assertIsInstance(path1, FlowPath)
        self.assertEqual("a.b.c", path1)


if __name__ == "__main__":
    main()
