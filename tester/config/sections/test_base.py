# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import TestCase, main

# noinspection PyProtectedMember
from cvp.config._base import BaseConfig

# noinspection PyProtectedMember
from cvp.config.sections._base import BaseSection

_TEST_INI_CONTENT = """
[sec]
key1 = False
key2 = 1
"""


class BaseTestCase(TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.assertTrue(os.path.isdir(self.temp_dir.name))

        self.test_ini = os.path.join(self.temp_dir.name, "test.ini")
        self.assertFalse(os.path.exists(self.test_ini))

        with open(self.test_ini, "w") as f:
            f.write(_TEST_INI_CONTENT)

        self.assertTrue(os.path.isfile(self.test_ini))

    def tearDown(self):
        self.temp_dir.cleanup()
        self.assertFalse(os.path.exists(self.temp_dir.name))

    def test_default(self):
        config = BaseConfig()
        config.read(self.test_ini)

        section1 = BaseSection(config, "sec")
        self.assertTrue(section1)
        self.assertEqual("sec", section1.section)
        self.assertSetEqual({"key1", "key2"}, set(section1.options()))
        self.assertIn("key1", section1)
        self.assertIn("key2", section1)
        self.assertNotIn("key3", section1)
        self.assertEqual(2, len(section1))

        o = section1.dumps()

        section2 = BaseSection(config, "Unknown")
        section2.extends(o)
        self.assertEqual(section1, section2)

        section2.clear()
        self.assertFalse(section2.dumps())


if __name__ == "__main__":
    main()
