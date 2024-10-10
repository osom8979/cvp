# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from cvp.keyring.keyring import (
    KEYRING_PLAIN_TEXT,
    KEYRING_SAGECIPHER,
    delete_password,
    get_keyring,
    get_password,
    keyring_context,
    list_keyring_names,
    load_keyring,
    set_keyring,
    set_password,
)


class KeyringTestCase(TestCase):
    def test_list_keyring_names(self):
        actual_backends = set(list_keyring_names())
        self.assertIn(KEYRING_PLAIN_TEXT, actual_backends)
        self.assertIn(KEYRING_SAGECIPHER, actual_backends)

    def test_keyring_context(self):
        prev_backend = get_keyring()
        with keyring_context():
            keyring = load_keyring(KEYRING_PLAIN_TEXT)
            set_keyring(keyring)
            self.assertEqual(keyring, get_keyring())
        self.assertEqual(prev_backend, get_keyring())

    def test_backends(self):
        for backend_name in (KEYRING_PLAIN_TEXT, KEYRING_SAGECIPHER):
            with TemporaryDirectory() as tmp:
                self.assertTrue(os.path.isdir(tmp))

                with keyring_context(backend_name) as backend:
                    keyring_filepath = os.path.join(tmp, "keyring.cfg")
                    self.assertFalse(os.path.exists(keyring_filepath))

                    type(backend).file_path = keyring_filepath
                    service = "test"
                    username = "cvp"
                    password = "pass"

                    self.assertIsNone(get_password(service, username))
                    set_password(service, username, password)
                    self.assertTrue(os.path.isfile(keyring_filepath))

                    self.assertEqual(password, get_password(service, username))
                    delete_password(service, username)
                    self.assertIsNone(get_password(service, username))


if __name__ == "__main__":
    main()
