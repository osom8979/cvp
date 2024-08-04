# -*- coding: utf-8 -*-

import os
from unittest import TestCase, main, skipIf

from cvp.ffmpeg.executable import (
    get_ffmpeg_executable,
    get_ffprobe_executable,
    has_ffmpeg,
    has_ffprobe,
)


class ExecutableTestCase(TestCase):
    @skipIf(has_ffmpeg(), "Already ffmpeg executable")
    def test_ffmpeg_executable(self):
        path = get_ffmpeg_executable()
        self.assertTrue(os.path.isfile(path))
        self.assertTrue(os.access(path, os.X_OK))

    @skipIf(has_ffprobe(), "Already ffprobe executable")
    def test_ffprobe_executable(self):
        path = get_ffprobe_executable()
        self.assertTrue(os.path.isfile(path))
        self.assertTrue(os.access(path, os.X_OK))


if __name__ == "__main__":
    main()
