# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import StrEnum, auto, unique
from typing import Optional
from uuid import uuid4

from cvp.config.sections.bases.manager import ManagerWindowConfig


@unique
class HttpAuth(StrEnum):
    basic = auto()
    digest = auto()


@dataclass
class OnvifConfig:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default_factory=str)
    address: str = field(default_factory=str)
    use_wsse: bool = False
    username: str = field(default_factory=str)
    # 'password' is stored in the keyring.
    encode_digest: bool = False
    http_auth: Optional[HttpAuth] = None
    no_verify: bool = False

    @property
    def is_http_basic(self):
        return self.http_auth == HttpAuth.basic

    @property
    def is_http_digest(self):
        return self.http_auth == HttpAuth.digest


@dataclass
class OnvifManagerConfig(ManagerWindowConfig):
    pass
