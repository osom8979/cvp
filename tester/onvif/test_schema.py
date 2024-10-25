# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.onvif.schema import OnvifSchema


class SchemaTestCase(TestCase):
    def setUp(self):
        self.schema = OnvifSchema()

    def test_onvif(self):
        namespaces = self.schema.onvif.namespaces
        documents = [d for d in self.schema.onvif.documents]
        elements = [e for e in self.schema.onvif.elements]
        types = [t for t in self.schema.onvif.types]
        self.assertIsInstance(namespaces, list)
        self.assertIsInstance(documents, list)
        self.assertIsInstance(elements, list)
        self.assertIsInstance(types, list)


if __name__ == "__main__":
    main()
