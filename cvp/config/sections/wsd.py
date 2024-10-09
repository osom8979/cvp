# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import StrEnum, auto, unique
from uuid import uuid4

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
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default_factory=str)


@dataclass
class WsdManagerConfig(ManagerWindowConfig):
    protocol: WsdProtocol = WsdProtocol.udp
    ipv4_address: str = WSD_IPV4_MULTICAST_ADDRESS
    ipv6_address: str = WSD_IPV6_MULTICAST_ADDRESS
    port: int = WSD_PORT_NUMBER
    timeout: float = WSD_TIMEOUT
