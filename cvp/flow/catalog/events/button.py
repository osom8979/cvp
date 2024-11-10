# -*- coding: utf-8 -*-

from cvp.flow.datas import NodeTemplate, PinTemplate


class ButtonEventNode(NodeTemplate):
    def __init__(self):
        super().__init__(
            name=type(self).__name__,
            docs="Button Event Node",
            pins=[PinTemplate()],
            tags=["event"],
        )
