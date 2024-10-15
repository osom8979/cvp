# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique


@unique
class TransportProtocol(StrEnum):
    UDP = auto()
    TCP = auto()  # Deprecated
    RTSP = auto()
    HTTP = auto()


@unique
class StreamType(StrEnum):
    RTPUnicast = "RTP-Unicast"
    RTPMulticast = "RTP-Multicast"
