# -*- coding: utf-8 -*-

from abc import ABCMeta
from typing import Optional

from cvp.msgs.abc import abstractmsg
from cvp.msgs.msg import MsgType


class MsgInterface(metaclass=ABCMeta):
    @abstractmsg(MsgType.none)
    def on_msg_none(self, uuid: str) -> Optional[bool]:
        raise NotImplementedError
