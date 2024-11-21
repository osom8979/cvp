# -*- coding: utf-8 -*-

from argparse import Namespace
from typing import Any, Dict, Optional
from uuid import uuid4

from cvp.inspect.member import get_public_instance_attributes
from cvp.msgs.msg_type import (
    MsgType,
    MsgTypeLike,
    get_msg_type_name,
    normalize_msg_type,
)


class Msg(Namespace):
    def __init__(
        self,
        mtype: Optional[MsgTypeLike] = None,
        uuid: Optional[str] = None,
        **kwargs,
    ):
        if "_mtype" in kwargs:
            raise KeyError("The '_mtype' attribute must not be specified")
        if "_uuid" in kwargs:
            raise KeyError("The '_uuid' attribute must not be specified")

        super().__init__(**kwargs)

        self._mtype = normalize_msg_type(mtype) if mtype is not None else MsgType.none
        self._uuid = uuid if uuid else str(uuid4())

    @property
    def mtype(self) -> MsgType:
        return self._mtype

    @property
    def uuid(self) -> str:
        return self._uuid

    def get_type_name(self) -> str:
        return get_msg_type_name(self.mtype)

    def as_args(self) -> Dict[str, Any]:
        return dict(get_public_instance_attributes(self))
