# -*- coding: utf-8 -*-

from typing import Any

from cvp.flow.arc import FlowArc, FlowArcKeys


class FlowArcBuilder:
    def __init__(self, **kwargs: Any):
        self.kwargs = kwargs

    def arc_clear(self):
        self.kwargs.clear()

    def arc_done(self):
        try:
            return FlowArc(**self.kwargs)
        finally:
            self.kwargs.clear()

    def arc_name(self, value: str):
        self.kwargs[FlowArcKeys.class_name] = value
        return self

    def arc_docs(self, value: str):
        self.kwargs[FlowArcKeys.class_docs] = value
        return self

    def arc_icon(self, value: str):
        self.kwargs[FlowArcKeys.class_icon] = value
        return self

    def arc_color(self, value: str):
        self.kwargs[FlowArcKeys.class_color] = value
        return self
