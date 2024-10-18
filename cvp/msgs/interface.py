# -*- coding: utf-8 -*-

from abc import ABCMeta
from typing import Any, Optional

from cvp.msgs.abc import abstractmsg
from cvp.msgs.msg_type import MsgType


class MsgInterface(metaclass=ABCMeta):
    @abstractmsg(MsgType.none)
    def on_msg_none(
        self,
        uuid: str,
        data: Any,
        error: Optional[BaseException],
    ) -> Optional[bool]:
        raise NotImplementedError
