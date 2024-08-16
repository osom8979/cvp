# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.ffmpeg.ffmpeg.builder import FFmpegBuilder


class BuilderTestCase(TestCase):
    def test_default(self):
        builder = FFmpegBuilder()
        self.assertIsNotNone(builder)


if __name__ == "__main__":
    main()
