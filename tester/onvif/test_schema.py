# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.onvif.schema import OnvifSchema


class SchemaTestCase(TestCase):
    def setUp(self):
        self.schema = OnvifSchema()

    def test_simple_types(self):
        simple_type_names = self.schema.simple_type_names
        self.assertTrue(simple_type_names)

    def test_complex_type(self):
        complex_type_names = self.schema.complex_type_names
        self.assertTrue(complex_type_names)

    def test_stream_type(self):
        types = self.schema.get_enumerations("StreamType")
        self.assertSetEqual({"RTP-Unicast", "RTP-Multicast"}, set(types))


if __name__ == "__main__":
    main()
