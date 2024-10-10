# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import StrEnum, auto, unique
from typing import List

from cvp.config.sections.bases.manager import ManagerWindowConfig
from cvp.variables import (
    WSD_IPV4_MULTICAST_ADDRESS,
    WSD_IPV6_MULTICAST_ADDRESS,
    WSD_PORT_NUMBER,
    WSD_TIMEOUT,
)


@unique
class WsdProtocol(StrEnum):
    tcp = auto()
    udp = auto()


@dataclass
class WsdConfig:
    epr: str = field(default_factory=str)
    instance_id: int = -1
    message_number: int = -1
    metadata_version: int = -1
    scopes: List[str] = field(default_factory=list)
    types: List[str] = field(default_factory=list)
    xaddrs: List[str] = field(default_factory=list)
    name: str = field(default_factory=str)

    def has_onvif_scope(self) -> bool:
        if not self.scopes:
            return False
        for scope in self.scopes:
            if scope.startswith("onvif://"):
                return True
        return False


@dataclass
class WsdManagerConfig(ManagerWindowConfig):
    protocol: WsdProtocol = WsdProtocol.udp
    ipv4_address: str = WSD_IPV4_MULTICAST_ADDRESS
    ipv6_address: str = WSD_IPV6_MULTICAST_ADDRESS
    port: int = WSD_PORT_NUMBER
    timeout: float = WSD_TIMEOUT
