# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.flow.datas.action import Action
from cvp.flow.datas.constants import EMPTY_TEXT
from cvp.flow.datas.stream import Stream


@dataclass
class PinTemplate:
    name: str = EMPTY_TEXT
    docs: str = EMPTY_TEXT
    dtype: str = EMPTY_TEXT
    action: Action = Action.data
    stream: Stream = Stream.input
    required: bool = False
