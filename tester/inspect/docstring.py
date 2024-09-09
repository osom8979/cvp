# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.inspect.docstring import get_attribute_docstring


class DocstringSample:
    blend_strength: int
    """Blend Strength"""

    mode_index: int
    """Mode index"""


class DocstringTestCase(TestCase):
    def test_get_attribute_docstring(self):
        doc0 = get_attribute_docstring(DocstringSample, "blend_strength")
        self.assertEqual("Blend Strength", doc0)

        doc1 = get_attribute_docstring(DocstringSample, "mode_index")
        self.assertEqual("Mode index", doc1.split("\n")[0])


if __name__ == "__main__":
    main()
