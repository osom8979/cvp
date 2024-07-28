# -*- coding: utf-8 -*-

import os
from tempfile import mkdtemp, mkstemp
from unittest import TestCase, main

from cvp.filesystem.permission import (
    change_executable,
    change_readable,
    change_writable,
    is_executable_dir,
    is_executable_file,
    is_readable_dir,
    is_readable_file,
    is_writable_dir,
    is_writable_file,
)


def _create_temp_file() -> str:
    fd, name = mkstemp()
    os.close(fd)
    return name


class PermissionTestCase(TestCase):
    def test_readable_file(self):
        path = _create_temp_file()
        try:
            change_readable(path)
            self.assertTrue(os.path.exists(path))
            self.assertTrue(is_readable_file(path))
            self.assertFalse(is_writable_file(path))
            self.assertFalse(is_executable_file(path))
            self.assertFalse(is_readable_dir(path))
            self.assertFalse(is_writable_dir(path))
            self.assertFalse(is_executable_dir(path))
        finally:
            os.remove(path)
        self.assertFalse(os.path.exists(path))

    def test_writable_file(self):
        path = _create_temp_file()
        try:
            change_writable(path)
            self.assertTrue(os.path.exists(path))
            self.assertFalse(is_readable_file(path))
            self.assertTrue(is_writable_file(path))
            self.assertFalse(is_executable_file(path))
            self.assertFalse(is_readable_dir(path))
            self.assertFalse(is_writable_dir(path))
            self.assertFalse(is_executable_dir(path))
        finally:
            os.remove(path)
        self.assertFalse(os.path.exists(path))

    def test_executable_file(self):
        path = _create_temp_file()
        try:
            change_executable(path)
            self.assertTrue(os.path.exists(path))
            self.assertFalse(is_readable_file(path))
            self.assertFalse(is_writable_file(path))
            self.assertTrue(is_executable_file(path))
            self.assertFalse(is_readable_dir(path))
            self.assertFalse(is_writable_dir(path))
            self.assertFalse(is_executable_dir(path))
        finally:
            os.remove(path)
        self.assertFalse(os.path.exists(path))

    def test_readable_dir(self):
        path = mkdtemp()
        try:
            change_readable(path)
            self.assertTrue(os.path.exists(path))
            self.assertFalse(is_readable_file(path))
            self.assertFalse(is_writable_file(path))
            self.assertFalse(is_executable_file(path))
            self.assertTrue(is_readable_dir(path))
            self.assertFalse(is_writable_dir(path))
            self.assertFalse(is_executable_dir(path))
        finally:
            os.rmdir(path)
        self.assertFalse(os.path.exists(path))

    def test_writable_dir(self):
        path = mkdtemp()
        try:
            change_writable(path)
            self.assertTrue(os.path.exists(path))
            self.assertFalse(is_readable_file(path))
            self.assertFalse(is_writable_file(path))
            self.assertFalse(is_executable_file(path))
            self.assertFalse(is_readable_dir(path))
            self.assertTrue(is_writable_dir(path))
            self.assertFalse(is_executable_dir(path))
        finally:
            os.rmdir(path)
        self.assertFalse(os.path.exists(path))

    def test_executable_dir(self):
        path = mkdtemp()
        try:
            change_executable(path)
            self.assertTrue(os.path.exists(path))
            self.assertFalse(is_readable_file(path))
            self.assertFalse(is_writable_file(path))
            self.assertFalse(is_executable_file(path))
            self.assertFalse(is_readable_dir(path))
            self.assertFalse(is_writable_dir(path))
            self.assertTrue(is_executable_dir(path))
        finally:
            os.rmdir(path)
        self.assertFalse(os.path.exists(path))


if __name__ == "__main__":
    main()
