# -*- coding: utf-8 -*-

from typing import Any, Optional

from cvp.msgs.interface import MsgInterface
from cvp.types.override import override


class MsgCallbacks(MsgInterface):
    @override
    def on_msg_none(
        self,
        uuid: str,
        data: Any,
        error: Optional[BaseException],
    ) -> Optional[bool]:
        pass
