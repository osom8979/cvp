# -*- coding: utf-8 -*-

import collections
from inspect import signature
from typing import Annotated, Any, List, Optional, Sequence, Union
from unittest import TestCase, main

from cvp.inspect.argument import Argument


class ArgumentTestCase(TestCase):
    def test_annotated_parameter(self):
        def _func(arg0: Annotated[int, "Query0", "Query1"]):
            return arg0

        sig = signature(_func)
        self.assertEqual(1, len(sig.parameters))
        argument = Argument(sig.parameters["arg0"])
        self.assertTrue(argument.is_empty_default)
        self.assertFalse(argument.is_empty_annotation)
        self.assertTrue(argument.is_annotated)
        self.assertEqual(argument.type_deduction(), int)
        self.assertEqual(3, len(argument.annotated_args))
        self.assertEqual(int, argument.annotated_args[0])
        self.assertEqual("Query0", argument.annotated_args[1])
        self.assertEqual("Query1", argument.annotated_args[2])

    def test_annotated_parameter_with_default(self):
        def _func(arg0: Annotated[int, "Query2"] = 100):
            return arg0

        sig = signature(_func)
        self.assertEqual(1, len(sig.parameters))
        argument = Argument(sig.parameters["arg0"])
        self.assertFalse(argument.is_empty_default)
        self.assertFalse(argument.is_empty_annotation)
        self.assertTrue(argument.is_annotated)
        self.assertEqual(argument.type_deduction(), int)
        self.assertEqual(2, len(argument.annotated_args))
        self.assertEqual(int, argument.annotated_args[0])
        self.assertEqual("Query2", argument.annotated_args[1])
        self.assertEqual(100, argument.default)

    def test_trivial_type(self):
        def _func(arg0: int):
            return arg0

        sig = signature(_func)
        self.assertEqual(1, len(sig.parameters))
        argument = Argument(sig.parameters["arg0"])
        self.assertTrue(argument.is_empty_default)
        self.assertFalse(argument.is_empty_annotation)
        self.assertFalse(argument.is_annotated)
        self.assertEqual(argument.type_deduction(), int)
        self.assertRaises(TypeError, lambda: argument.annotated_args)

    def test_trivial_type_with_default(self):
        def _func(arg0: int = 200):
            return arg0

        sig = signature(_func)
        self.assertEqual(1, len(sig.parameters))
        argument = Argument(sig.parameters["arg0"])
        self.assertFalse(argument.is_empty_default)
        self.assertFalse(argument.is_empty_annotation)
        self.assertFalse(argument.is_annotated)
        self.assertEqual(argument.type_deduction(), int)
        self.assertRaises(TypeError, lambda: argument.annotated_args)
        self.assertEqual(200, argument.default)

    def test_default_value(self):
        def _func(arg0=1):
            return arg0

        sig = signature(_func)
        self.assertEqual(1, len(sig.parameters))
        argument = Argument(sig.parameters["arg0"])
        self.assertFalse(argument.is_empty_default)
        self.assertTrue(argument.is_empty_annotation)
        self.assertFalse(argument.is_annotated)
        self.assertEqual(argument.type_deduction(), int)
        self.assertRaises(TypeError, lambda: argument.annotated_args)
        self.assertEqual(1, argument.default)

    def test_any(self):
        def _func(arg0: Any):
            return arg0

        sig = signature(_func)
        self.assertEqual(1, len(sig.parameters))
        argument = Argument(sig.parameters["arg0"])
        self.assertTrue(argument.is_empty_default)
        self.assertFalse(argument.is_empty_annotation)
        self.assertFalse(argument.is_annotated)
        self.assertEqual(argument.type_deduction(), Any)
        self.assertRaises(TypeError, lambda: argument.annotated_args)

    def test_list(self):
        def _func(arg0: List[int]):
            return arg0

        sig = signature(_func)
        self.assertEqual(1, len(sig.parameters))
        argument = Argument(sig.parameters["arg0"])
        self.assertTrue(argument.is_empty_default)
        self.assertFalse(argument.is_empty_annotation)
        self.assertFalse(argument.is_annotated)
        self.assertEqual(argument.type_deduction(), list)
        self.assertRaises(TypeError, lambda: argument.annotated_args)

    def test_sequence(self):
        def _func(arg0: Sequence[int]):
            return arg0

        sig = signature(_func)
        self.assertEqual(1, len(sig.parameters))
        argument = Argument(sig.parameters["arg0"])
        self.assertTrue(argument.is_empty_default)
        self.assertFalse(argument.is_empty_annotation)
        self.assertFalse(argument.is_annotated)
        self.assertEqual(argument.type_deduction(), collections.abc.Sequence)
        self.assertRaises(TypeError, lambda: argument.annotated_args)

    def test_optional(self):
        def _func(arg0: Optional[int]):
            return arg0

        sig = signature(_func)
        self.assertEqual(1, len(sig.parameters))
        argument = Argument(sig.parameters["arg0"])
        self.assertTrue(argument.is_empty_default)
        self.assertFalse(argument.is_empty_annotation)
        self.assertFalse(argument.is_annotated)
        self.assertEqual(argument.type_deduction(), Union)
        self.assertRaises(TypeError, lambda: argument.annotated_args)

    def test_union(self):
        def _func(arg0: Union[int, float]):
            return arg0

        sig = signature(_func)
        self.assertEqual(1, len(sig.parameters))
        argument = Argument(sig.parameters["arg0"])
        self.assertTrue(argument.is_empty_default)
        self.assertFalse(argument.is_empty_annotation)
        self.assertFalse(argument.is_annotated)
        self.assertEqual(argument.type_deduction(), Union)
        self.assertRaises(TypeError, lambda: argument.annotated_args)

    def test_none(self):
        def _func(arg0=None):
            return arg0

        sig = signature(_func)
        self.assertEqual(1, len(sig.parameters))
        argument = Argument(sig.parameters["arg0"])
        self.assertFalse(argument.is_empty_default)
        self.assertTrue(argument.is_empty_annotation)
        self.assertFalse(argument.is_annotated)
        self.assertEqual(argument.type_deduction(), type(None))
        self.assertRaises(TypeError, lambda: argument.annotated_args)
        self.assertIsNone(argument.default)

    def test_unknown(self):
        def _func(arg0):
            return arg0

        sig = signature(_func)
        self.assertEqual(1, len(sig.parameters))
        argument = Argument(sig.parameters["arg0"])
        self.assertTrue(argument.is_empty_default)
        self.assertTrue(argument.is_empty_annotation)
        self.assertFalse(argument.is_annotated)
        self.assertEqual(argument.type_deduction(), object)
        self.assertRaises(TypeError, lambda: argument.annotated_args)

    def test_manual_initialize(self):
        argument = Argument.from_details(
            name="args0",
            default=20,
            annotation=Annotated[str, "Query0"],
        )
        self.assertFalse(argument.is_empty_default)
        self.assertFalse(argument.is_empty_annotation)
        self.assertTrue(argument.is_annotated)
        self.assertEqual(argument.type_deduction(), str)
        self.assertEqual(2, len(argument.annotated_args))
        self.assertEqual(str, argument.annotated_args[0])
        self.assertEqual("Query0", argument.annotated_args[1])
        self.assertEqual(20, argument.default)


if __name__ == "__main__":
    main()
