# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.fonts.ranges import CodepointRange


class RangesTestCase(TestCase):
    def test_blocks_1(self):
        self.assertListEqual([(0x00, 0xFF)], CodepointRange(0x00, 0x00).as_blocks())
        self.assertListEqual([(0x00, 0xFF)], CodepointRange(0x00, 0x01).as_blocks())
        self.assertListEqual([(0x00, 0xFF)], CodepointRange(0x01, 0x01).as_blocks())
        self.assertListEqual([(0x00, 0xFF)], CodepointRange(0x01, 0xFE).as_blocks())
        self.assertListEqual([(0x00, 0xFF)], CodepointRange(0x01, 0xFF).as_blocks())
        self.assertListEqual([(0x00, 0xFF)], CodepointRange(0xFE, 0xFF).as_blocks())
        self.assertListEqual([(0x00, 0xFF)], CodepointRange(0xFF, 0xFF).as_blocks())

    def test_blocks_2(self):
        block1 = CodepointRange(0x00, 0x100).as_blocks()
        self.assertListEqual([(0x00, 0xFF), (0x100, 0x1FF)], block1)

        block2 = CodepointRange(0x01, 0x100).as_blocks()
        self.assertListEqual([(0x00, 0xFF), (0x100, 0x1FF)], block2)

        block3 = CodepointRange(0xFF, 0x100).as_blocks()
        self.assertListEqual([(0x00, 0xFF), (0x100, 0x1FF)], block3)

        block4 = CodepointRange(0x100, 0x100).as_blocks()
        self.assertListEqual([(0x100, 0x1FF)], block4)

        block5 = CodepointRange(0x100, 0x2FF).as_blocks()
        self.assertListEqual([(0x100, 0x1FF), (0x200, 0x2FF)], block5)

        block6 = CodepointRange(0x100, 0x300).as_blocks()
        self.assertListEqual([(0x100, 0x1FF), (0x200, 0x2FF), (0x300, 0x3FF)], block6)


if __name__ == "__main__":
    main()
