# -*- coding: utf-8 -*-

from unittest import TestCase, main, skipIf

from cvp.ffmpeg.executable.which import which_ffmpeg
from cvp.process.thread import PopenThread


class ThreadTestCase(TestCase):
    @skipIf(which_ffmpeg() is None, "Not found ffmpeg executable")
    def test_default(self):
        def _runnable() -> None:
            pass

        ffmpeg = which_ffmpeg()
        self.assertIsInstance(ffmpeg, str)

        args = (
            ffmpeg,
            "-f",
            "lavfi",
            "-i",
            "color=c=red:duration=5:size=1920x1080:rate=10",
            "-pix_fmt",
            "rgb24",
            "-f",
            "rawvideo",
            "pipe:",
        )
        popen = PopenThread(name=type(self).__name__, args=args, target=_runnable)

        buffer = list()
        try:
            while True:
                if popen.process.stdout.closed:
                    print("stdout closed -> break")
                    break

                return_code = popen.process.poll()
                if return_code is not None:
                    print(f"return code is {return_code} -> break")
                    break

                data = popen.process.stdout.read(1920 * 1080 * 3)
                if len(data) == 0:
                    print("data is 0 -> continue")
                    continue

                print(f"Recv: {len(data)} ...")
                buffer.append(data)
        except BaseException as e:
            print(e)

        self.assertEqual(50, len(buffer))


if __name__ == "__main__":
    main()
