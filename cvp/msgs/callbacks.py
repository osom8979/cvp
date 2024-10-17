# -*- coding: utf-8 -*-

from typing import Optional

from cvp.msgs.interface import MsgInterface
from cvp.types import override


class MsgCallbacks(MsgInterface):
    @override
    def on_msg_none(self, uuid: str) -> Optional[bool]:
        pass
