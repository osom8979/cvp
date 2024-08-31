# -*- coding: utf-8 -*-

import os
from tempfile import NamedTemporaryFile, TemporaryDirectory
from unittest import TestCase, main

from cvp.buffers.lines import LinesBuffer


class LinesTestCase(TestCase):
    def test_default(self):
        with TemporaryDirectory() as tmpdir:
            self.assertTrue(os.path.isdir(tmpdir))

            with NamedTemporaryFile("wt", dir=tmpdir) as f:
                with LinesBuffer(f.name, maxlen=2) as buffer:
                    self.assertEqual(5, f.write("12345"))

                    # ------------------------------------------------------------------
                    # [IMPORTANT]
                    # If you want to create a memory-mapping for a writable,
                    # buffered file, you should flush() the file first.
                    # This is necessary to ensure that local modifications to the
                    # buffers are actually available to the mapping.
                    f.flush()
                    # ------------------------------------------------------------------

                    self.assertEqual(5, os.path.getsize(f.name))

                    buffer.update()
                    self.assertEqual(1, len(buffer.lines))
                    self.assertEqual("12345", buffer.lines[0])

                    self.assertEqual(5, f.write("67890"))
                    f.flush()
                    self.assertEqual(10, os.path.getsize(f.name))

                    buffer.update()
                    self.assertEqual(1, len(buffer.lines))
                    self.assertEqual("1234567890", buffer.lines[0])

                    self.assertEqual(6, f.write("\nabcde"))
                    f.flush()
                    self.assertEqual(16, os.path.getsize(f.name))

                    buffer.update()
                    self.assertEqual(2, len(buffer.lines))
                    self.assertEqual("1234567890", buffer.lines[0])
                    self.assertEqual("abcde", buffer.lines[1])

                    self.assertEqual(10, f.write("-zxcv\nqwer"))
                    f.flush()
                    self.assertEqual(26, os.path.getsize(f.name))

                    buffer.update()
                    self.assertEqual(2, len(buffer.lines))
                    self.assertEqual("abcde-zxcv", buffer.lines[0])
                    self.assertEqual("qwer", buffer.lines[1])

                    self.assertEqual(1, f.write("\n"))
                    f.flush()
                    self.assertEqual(27, os.path.getsize(f.name))

                    buffer.update()
                    self.assertEqual(2, len(buffer.lines))
                    self.assertEqual("qwer", buffer.lines[0])
                    self.assertEqual("", buffer.lines[1])


if __name__ == "__main__":
    main()
