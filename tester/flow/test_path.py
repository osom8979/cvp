# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.flow.path import FlowPath


class PathTestCase(TestCase):
    def test_normalize(self):
        path = FlowPath("a.b.c.d.")
        self.assertEqual("a.b.c.d", path.normalize())

    def test_split(self):
        path = FlowPath("a.b.c.d")
        self.assertEqual("a.b.c", path.get_module_path())
        self.assertEqual("d", path.get_node_name())

    def test_join(self):
        path = FlowPath("a.b.c.")
        path2 = path.join("key")
        self.assertEqual("a.b.c.key", path2)


if __name__ == "__main__":
    main()
