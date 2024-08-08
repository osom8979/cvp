# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import TestCase, main

# noinspection PyProtectedMember
from cvp.config._base import BaseConfig

_TEST_INI_CONTENT = """
[Window][Debug##Default]
Size=400,400
# Comment
[Window][Open Network Stream]
Collapsed=0
Latest=${HOME}

[display]
fullscreen = False  # Not comment
color = 0.5, 0.5, 0.5

[av.1]
opened = "False"  ; Not comment

[av.2]
opened = 1
"""

_EXPECTED_SECTIONS = {
    "Window][Debug##Default",
    "Window][Open Network Stream",
    "display",
    "av.1",
    "av.2",
}

_EXPECTED_SERIALIZED_OBJECT = {
    "Window][Debug##Default": {"size": "400,400"},
    "Window][Open Network Stream": {"collapsed": "0", "latest": "${HOME}"},
    "display": {"fullscreen": "False  # Not comment", "color": "0.5, 0.5, 0.5"},
    "av.1": {"opened": '"False"  ; Not comment'},
    "av.2": {"opened": "1"},
}


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
        self.assertFalse(config)

        config.set_config_value("A", "B", "1")
        self.assertTrue(config)
        self.assertEqual(1, len(config))

        for item in config:
            self.assertTupleEqual(("A", "b", "1"), item)  # It only hits once.

        self.assertEqual("1", config.get_config_value("A", "B", "?"))
        self.assertEqual("?", config.get_config_value("A", "C", "?"))

        self.assertTrue(config.has("A", "B"))
        self.assertFalse(config.has("A", "C"))
        self.assertFalse(config.has("a", "B"))

        self.assertIn(("A", "B"), config)
        self.assertNotIn(("A", "C"), config)
        self.assertNotIn(("a", "B"), config)

        self.assertSetEqual({"A"}, set(config.sections()))
        self.assertSetEqual({"b"}, set(config.options("A")))

        self.assertIsInstance(config.get("A", "B"), str)
        self.assertIsInstance(config.get("A", "B", 0), int)
        self.assertIsInstance(config.get("A", "B", 0.0), float)
        self.assertIsInstance(config.get("A", "B", False), bool)

        self.assertEqual("1", config.get("A", "B"))
        self.assertEqual(1, config.get("A", "B", 0))
        self.assertEqual(1.0, config.get("A", "B", 0.0))
        self.assertEqual(True, config.get("A", "B", False))

        config.clear()
        self.assertFalse(config)

    def test_read_write(self):
        config1 = BaseConfig()
        config1.read(self.test_ini)

        temp_ini = os.path.join(self.temp_dir.name, "temp.ini")
        self.assertFalse(os.path.exists(temp_ini))

        config1.write(temp_ini)
        self.assertTrue(os.path.isfile(temp_ini))

        config2 = BaseConfig()
        config2.read(temp_ini)
        self.assertEqual(config1, config2)

    def test_dumps_extends(self):
        config1 = BaseConfig(self.test_ini)
        self.assertSetEqual(_EXPECTED_SECTIONS, set(config1.sections()))

        o = config1.dumps()
        self.assertDictEqual(_EXPECTED_SERIALIZED_OBJECT, o)

        config2 = BaseConfig()
        config2.extends(o)
        self.assertEqual(config1, config2)

        config2.clear()
        self.assertFalse(config2.dumps())


if __name__ == "__main__":
    main()
