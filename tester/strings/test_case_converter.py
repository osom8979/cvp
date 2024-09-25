# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.strings.case_converter import camelcase_to_snakecase


class CaseConverterTestCase(TestCase):
    def test_camelcase_to_snakecase(self):
        self.assertEqual(
            "camel_case_example",
            camelcase_to_snakecase("CamelCaseExample"),
        )
        self.assertEqual(
            "camel_case_example",
            camelcase_to_snakecase("CAMELCaseExample"),
        )
        self.assertEqual(
            "camel_case_example",
            camelcase_to_snakecase("CamelCASEExample"),
        )
        self.assertEqual(
            "camel_case_example",
            camelcase_to_snakecase("CamelCaseEXAMPLE"),
        )
        self.assertEqual(
            "camel_case_example",
            camelcase_to_snakecase("Camel_CASE_Example"),
        )
        self.assertEqual(
            "_camel_case_example_",
            camelcase_to_snakecase("_CamelCaseExample_"),
        )
        self.assertEqual(
            "__camel_case_example__",
            camelcase_to_snakecase("__CamelCaseExample__"),
        )


if __name__ == "__main__":
    main()
