# -*- coding: utf-8 -*-

from abc import ABCMeta

from cvp.msgs.abc import abstractmsg
from cvp.msgs.msg_type import MsgType


class MsgInterface(metaclass=ABCMeta):
    @abstractmsg(MsgType.none)
    def on_msg_none(self):
        raise NotImplementedError

    @abstractmsg(MsgType.toast)
    def on_msg_toast(self, message: str):
        raise NotImplementedError
