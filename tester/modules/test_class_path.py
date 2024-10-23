# -*- coding: utf-8 -*-

from pathlib import Path
from unittest import TestCase, main

from cvp.modules.class_path import ClassPath


class ClassPathTestCase(TestCase):
    def test_default(self):
        cpath0 = ClassPath("pathlib.Path")
        cpath1 = ClassPath(Path)

        self.assertIsInstance(cpath0.type, type)
        self.assertIsInstance(cpath1.type, type)
        self.assertTrue(issubclass(cpath0.type, Path))
        self.assertTrue(issubclass(cpath1.type, Path))

        self.assertEqual(cpath0.type, cpath1.type)
        self.assertEqual(cpath0.path, cpath1.path)

        self.assertEqual(cpath0.path, "pathlib.Path")
        self.assertEqual(cpath1.path, "pathlib.Path")
        self.assertEqual(cpath0.module_path, "pathlib")
        self.assertEqual(cpath1.module_path, "pathlib")
        self.assertEqual(cpath0.class_name, "Path")
        self.assertEqual(cpath1.class_name, "Path")

        path0 = cpath0("./aaa")
        path1 = cpath1("./aaa")
        self.assertIsInstance(path0, Path)
        self.assertIsInstance(path1, Path)


if __name__ == "__main__":
    main()
