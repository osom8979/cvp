# -*- coding: utf-8 -*-

from enum import IntEnum, unique
from typing import Final, Optional, Union
from unittest import TestCase, main

from cvp.types.enum.normalize import (
    FrozenNameToNumber,
    FrozenNumberToName,
    name2number,
    normalize_name2number,
    normalize_number2name,
    number2name,
)


@unique
class _Test(IntEnum):
    value0 = 0
    value1 = 1


_DEFAULT_TEST_VALUE: Final[int] = _Test.value0.value
_DEFAULT_TEST_NAME: Final[str] = _Test.value0.name

_TEST_NAME2INDEX: Final[FrozenNameToNumber] = name2number(_Test)
_TEST_INDEX2NAME: Final[FrozenNumberToName] = number2name(_Test)


def normalize_test_value(value: Optional[Union[_Test, str, int]]) -> int:
    if value is None:
        return _DEFAULT_TEST_VALUE
    return normalize_name2number(_TEST_NAME2INDEX, value)


def normalize_test_name(value: Optional[Union[_Test, str, int]]) -> str:
    if value is None:
        return _DEFAULT_TEST_NAME
    return normalize_number2name(_TEST_INDEX2NAME, value)


class NormalizeTestCase(TestCase):
    def test_normalize_test_name(self):
        self.assertEqual("value0", normalize_test_name(None))
        self.assertEqual("value0", normalize_test_name(_Test.value0))
        self.assertEqual("value1", normalize_test_name(_Test.value1))
        self.assertEqual("value0", normalize_test_name("value0"))
        self.assertEqual("value1", normalize_test_name("value1"))
        self.assertEqual("value0", normalize_test_name(0))
        self.assertEqual("value1", normalize_test_name(1))

    def test_normalize_test_value(self):
        self.assertEqual(0, normalize_test_value(None))
        self.assertEqual(0, normalize_test_value(_Test.value0))
        self.assertEqual(1, normalize_test_value(_Test.value1))
        self.assertEqual(0, normalize_test_value("value0"))
        self.assertEqual(1, normalize_test_value("value1"))
        self.assertEqual(0, normalize_test_value(0))
        self.assertEqual(1, normalize_test_value(1))


if __name__ == "__main__":
    main()
