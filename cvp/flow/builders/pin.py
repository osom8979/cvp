# -*- coding: utf-8 -*-

from typing import Any, Union

from cvp.flow.enums.action import FlowAction, normalize_action_value
from cvp.flow.enums.stream import FlowStream, normalize_stream_value
from cvp.flow.pin import FlowPin, FlowPinKeys


class FlowPinBuilder:
    def __init__(self, **kwargs: Any):
        self.kwargs = kwargs

    def pin_clear(self):
        self.kwargs.clear()

    def pin_done(self):
        try:
            return FlowPin(**self.kwargs)
        finally:
            self.kwargs.clear()

    def pin_name(self, value: str):
        self.kwargs[FlowPinKeys.class_name] = value
        return self

    def pin_docs(self, value: str):
        self.kwargs[FlowPinKeys.class_docs] = value
        return self

    def pin_action(self, value: Union[FlowAction, str, int]):
        self.kwargs[FlowPinKeys.class_action] = normalize_action_value(value)
        return self

    def pin_action_flow(self):
        return self.pin_action(FlowAction.flow)

    def pin_action_data(self):
        return self.pin_action(FlowAction.data)

    def pin_stream(self, value: Union[FlowStream, str, int]):
        self.kwargs[FlowPinKeys.class_stream] = normalize_stream_value(value)
        return self

    def pin_stream_input(self):
        return self.pin_stream(FlowStream.input)

    def pin_stream_output(self):
        return self.pin_stream(FlowStream.output)

    def pin_dtype(self, value: str):
        self.kwargs[FlowPinKeys.class_dtype] = value
        return self

    def pin_required(self, value: str):
        self.kwargs[FlowPinKeys.class_required] = value
        return self

    def pin_exported(self, value: str):
        self.kwargs[FlowPinKeys.class_exported] = value
        return self

    def pin_icon(self, value: str):
        self.kwargs[FlowPinKeys.class_icon] = value
        return self

    def pin_color(self, value: str):
        self.kwargs[FlowPinKeys.class_color] = value
        return self
