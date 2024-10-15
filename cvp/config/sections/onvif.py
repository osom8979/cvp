# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import StrEnum, auto, unique
from typing import List, Optional
from uuid import uuid4

from cvp.config.sections.bases.manager import ManagerWindowConfig
from cvp.itertools.find_index import find_index


@unique
class HttpAuth(StrEnum):
    basic = auto()
    digest = auto()


@dataclass
class OnvifService:
    namespace: str = field(default_factory=str)
    xaddr: str = field(default_factory=str)
    version_major: int = 0
    version_minor: int = 0


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
    services: List[OnvifService] = field(default_factory=list)

    @property
    def is_http_basic(self):
        return self.http_auth == HttpAuth.basic

    @property
    def is_http_digest(self):
        return self.http_auth == HttpAuth.digest

    def find_service(self, namespace: str) -> int:
        return find_index(self.services, lambda x: x.namespace == namespace)


@dataclass
class OnvifManagerConfig(ManagerWindowConfig):
    pass
