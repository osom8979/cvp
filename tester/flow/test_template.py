# -*- coding: utf-8 -*-

from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.flow.pin import FlowPin, FlowStream, FlowType
from cvp.flow.template import FlowTemplate


class TemplateTestCase(TestCase):
    def test_serializable(self):
        i = FlowPin("i", FlowType.data, FlowStream.input, "int", "right", "#000")
        o = FlowPin("o", FlowType.flow, FlowStream.output, "float", "left", "#FFF")
        template = FlowTemplate("tmp", [i, o], "node", "#222")
        obj = serialize(template)
        result = deserialize(obj, FlowTemplate)
        self.assertEqual(template, result)

    def test_required_serializable(self):
        template = FlowTemplate("tmp")
        obj = serialize(template)
        self.assertIsInstance(obj, dict)
        self.assertListEqual([], obj.pop("pins"))
        self.assertEqual("", obj.pop("icon"))
        self.assertEqual("", obj.pop("color"))
        result = deserialize(obj, FlowTemplate)
        self.assertEqual(template, result)


if __name__ == "__main__":
    main()
