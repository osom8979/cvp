# -*- coding: utf-8 -*-
from typing import Any

from overrides import override

from cvp.flow.builders.pin import FlowPinBuilder
from cvp.flow.node import FlowNode, FlowNodeKeys
from cvp.flow.pin import FlowPin


class _FlowPinBuilderProxy(FlowPinBuilder):
    def __init__(self, parent: "FlowNodeBuilder", **kwargs: Any):
        super().__init__(**kwargs)
        self._parent = parent

    @override
    def pin_done(self):
        pins = self._parent.kwargs[FlowNodeKeys.class_pins]
        assert isinstance(pins, list)

        try:
            pins.append(FlowPin(**self.kwargs))
            return self._parent
        finally:
            self.kwargs.clear()


class FlowNodeBuilder:
    def __init__(self, **kwargs: Any):
        self.kwargs = kwargs

        if FlowNodeKeys.class_pins not in self.kwargs:
            self.kwargs[FlowNodeKeys.class_pins] = list()
        if FlowNodeKeys.class_tags not in self.kwargs:
            self.kwargs[FlowNodeKeys.class_tags] = list()

        assert isinstance(self.kwargs[FlowNodeKeys.class_pins], list)
        assert isinstance(self.kwargs[FlowNodeKeys.class_tags], list)

    def node_clear(self):
        self.kwargs.clear()
        self.kwargs[FlowNodeKeys.class_pins] = list()
        self.kwargs[FlowNodeKeys.class_tags] = list()

    def node_done(self):
        try:
            return FlowNode(**self.kwargs)
        finally:
            self.kwargs.clear()

    def node_name(self, value: str):
        self.kwargs[FlowNodeKeys.class_name] = value
        return self

    def node_docs(self, value: str):
        self.kwargs[FlowNodeKeys.class_docs] = value
        return self

    def node_icon(self, value: str):
        self.kwargs[FlowNodeKeys.class_icon] = value
        return self

    def node_color(self, value: str):
        self.kwargs[FlowNodeKeys.class_color] = value
        return self

    def node_create_pin(self, **kwargs: Any):
        assert FlowNodeKeys.class_pins in self.kwargs
        return _FlowPinBuilderProxy(self, **kwargs)

    def node_append_tag(self, value: str):
        assert FlowNodeKeys.class_tags in self.kwargs
        tags = self.kwargs[FlowNodeKeys.class_tags]
        assert isinstance(tags, list)
        tags.append(value)
        return self
