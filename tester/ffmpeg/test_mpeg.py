# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.ffmpeg.mpeg import FFmpegBuilder


class MpegTestCase(TestCase):
    def test_default(self):
        ffmpeg = FFmpegBuilder()
        self.assertIsNotNone(ffmpeg)


if __name__ == "__main__":
    main()
