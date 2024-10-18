# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from uuid import uuid4

from cvp.msgs.msg_type import MsgType, get_msg_type_name, get_msg_type_number


@dataclass
class Msg:
    type: MsgType = MsgType.none
    uuid: str = field(default_factory=lambda: str(uuid4()))
    data: Any = None
    error: Optional[BaseException] = None

    @property
    def number(self) -> int:
        return get_msg_type_number(self.type)

    @property
    def name(self) -> str:
        return get_msg_type_name(self.type)

    def as_args(self) -> Dict[str, Any]:
        return dict(uuid=self.uuid, data=self.data, error=self.error)
