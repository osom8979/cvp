# -*- coding: utf-8 -*-

import os
from unittest import TestCase, main

from cvp.system.environ import exchange_env_context


class EnvironTestCase(TestCase):
    def test_exchange(self):
        key = "__CVP_TEST_ENV_KEY__"
        original = "__CVP_TEST_ENV_ORI__"
        exchange = "__CVP_TEST_ENV_EX__"

        self.assertTrue(key not in os.environ)
        os.environ[key] = original

        try:
            self.assertEqual(original, os.environ.get(key))
            with exchange_env_context(key, exchange):
                self.assertEqual(exchange, os.environ.get(key))
            self.assertEqual(original, os.environ.get(key))
        finally:
            os.environ.pop(key)

        self.assertTrue(key not in os.environ)


if __name__ == "__main__":
    main()
