# -*- coding: utf-8 -*-

from cvp.flow.node import FlowNode
from cvp.flow.pin import FlowPin


class ButtonEventNode(FlowNode):
    def __init__(self):
        super().__init__(
            class_name=type(self).__name__,
            class_docs="Button Event Node",
            class_icon=None,
            class_color=None,
            class_pins=[FlowPin()],
            class_tags=["event"],
        )
