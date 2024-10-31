# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.onvif.schema import OnvifSchema


class SchemaTestCase(TestCase):
    def setUp(self):
        self.schema = OnvifSchema()

    def test_default(self):
        prefix = self.schema.root_prefix
        namespace = self.schema.root_namespace
        self.assertEqual("tt", prefix)
        self.assertEqual("http://www.onvif.org/ver10/schema", namespace)

    def test_types(self):
        simple_types = self.schema.simple_types
        complex_types = self.schema.complex_types
        types = self.schema.types

        self.assertEqual(109, len(simple_types))
        self.assertEqual(521, len(complex_types))
        self.assertEqual(len(types), len(simple_types) + len(complex_types))

    def test_names(self):
        types = set(q.localname for q in self.schema.types.keys())
        names = set(n for n in self.schema.names.keys())

        added_names = names - types
        removed_names = types - names

        self.assertSetEqual(set(), added_names)
        self.assertSetEqual(set(), removed_names)

    def test_stream_type(self):
        stream_type0 = self.schema["StreamType"]
        stream_type1 = self.schema[f"{self.schema.root_prefix}:StreamType"]
        stream_type2 = self.schema[f"{{{self.schema.root_namespace}}}StreamType"]
        stream_type3 = self.schema.get_root_type("StreamType")
        self.assertEqual(stream_type0, stream_type1)
        self.assertEqual(stream_type1, stream_type2)
        self.assertEqual(stream_type2, stream_type3)

    def test_get_enumeration_values(self):
        stream_type = self.schema.get_type("StreamType")
        values = self.schema.get_enumeration_values(stream_type)
        self.assertSetEqual({"RTP-Unicast", "RTP-Multicast"}, set(values))

    def test_time_zone(self):
        time_zone = self.schema.get_type("TimeZone")
        self.assertEqual("TimeZone", time_zone.attrib.get("name"))


if __name__ == "__main__":
    main()
