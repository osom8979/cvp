# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.flow.enums.stream import (
    FlowStream,
    normalize_stream_name,
    normalize_stream_value,
)


class StreamTestCase(TestCase):
    def test_normalize_stream_name(self):
        self.assertEqual("input", normalize_stream_name(None))
        self.assertEqual("input", normalize_stream_name(FlowStream.input))
        self.assertEqual("output", normalize_stream_name(FlowStream.output))
        self.assertEqual("input", normalize_stream_name("input"))
        self.assertEqual("output", normalize_stream_name("output"))
        self.assertEqual("input", normalize_stream_name(0))
        self.assertEqual("output", normalize_stream_name(1))

    def test_normalize_stream_value(self):
        self.assertEqual(0, normalize_stream_value(None))
        self.assertEqual(0, normalize_stream_value(FlowStream.input))
        self.assertEqual(1, normalize_stream_value(FlowStream.output))
        self.assertEqual(0, normalize_stream_value("input"))
        self.assertEqual(1, normalize_stream_value("output"))
        self.assertEqual(0, normalize_stream_value(0))
        self.assertEqual(1, normalize_stream_value(1))


if __name__ == "__main__":
    main()
