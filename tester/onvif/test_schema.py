# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.onvif.schema import OnvifSchema


class SchemaTestCase(TestCase):
    def setUp(self):
        self.schema = OnvifSchema()

    def test_types(self):
        simple_types = self.schema.simple_types
        complex_types = self.schema.complex_types
        types = self.schema.types
        self.assertEqual(len(types), len(simple_types) + len(complex_types))

    def test_stream_type(self):
        stream_types = self.schema.get_enumerations("StreamType")
        self.assertIsNotNone(stream_types)
        self.assertSetEqual({"RTP-Unicast", "RTP-Multicast"}, set(stream_types))


if __name__ == "__main__":
    main()
