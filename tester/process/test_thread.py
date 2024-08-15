# -*- coding: utf-8 -*-

from io import StringIO
from unittest import TestCase, main, skipIf

import numpy as np

from cvp.ffmpeg.executable.which import which_ffmpeg
from cvp.process.thread import PopenThread


class ThreadTestCase(TestCase):
    @skipIf(which_ffmpeg() is None, "Not found ffmpeg executable")
    def test_default(self):
        ffmpeg = which_ffmpeg()
        self.assertIsInstance(ffmpeg, str)

        duration = 3
        rate = 10
        width = 1920
        height = 1080
        channels = 3
        pix_fmt = "rgb24"
        frame_size = width * height * channels
        shape = height, width, channels
        total_frames = duration * rate
        color = 253, 0, 0  # red

        input_buffer = StringIO()
        input_buffer.write("color=")
        input_buffer.write("c=red")
        input_buffer.write(f":duration={duration}")
        input_buffer.write(f":size={width}x{height}")
        input_buffer.write(f":rate={rate}")
        input_file = input_buffer.getvalue()

        args = (
            ffmpeg,
            "-f",
            "lavfi",
            "-i",
            input_file,
            "-pix_fmt",
            pix_fmt,
            "-f",
            "rawvideo",
            "pipe:",
        )
        popen = PopenThread(name=type(self).__name__, args=args)

        frames = list()

        while True:
            return_code = popen.process.poll()
            if return_code is not None:
                break

            if popen.process.stdout.closed:
                break

            data = popen.process.stdout.read(frame_size)
            if len(data) == 0:
                continue

            frame = np.ndarray(shape, dtype=np.uint8, buffer=data)
            frames.append(frame)

        self.assertEqual(0, return_code)
        self.assertEqual(total_frames, len(frames))
        for frame in frames:
            self.assertTrue(np.all(frame[:, :] == color))


if __name__ == "__main__":
    main()
