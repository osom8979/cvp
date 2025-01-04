# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.flow.datas.action import Action
from cvp.flow.datas.stream import Stream


@dataclass
class PinTemplate:
    name: str = str()
    docs: str = str()
    dtype: str = str()
    action: Action = Action.data
    stream: Stream = Stream.input
    required: bool = False
