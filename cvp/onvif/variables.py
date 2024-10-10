# -*- coding: utf-8 -*-

from typing import Final, Sequence

ONVIF_V10_SCHEMA_URL: Final[str] = "http://www.onvif.org/ver10/schema"

TRANSPORT_PROTOCOL_UDP: Final[str] = "UDP"
TRANSPORT_PROTOCOL_TCP: Final[str] = "TCP"  # Deprecated
TRANSPORT_PROTOCOL_RTSP: Final[str] = "RTSP"
TRANSPORT_PROTOCOL_HTTP: Final[str] = "HTTP"
TRANSPORT_PROTOCOLS: Sequence[str] = (
    TRANSPORT_PROTOCOL_UDP,
    TRANSPORT_PROTOCOL_TCP,
    TRANSPORT_PROTOCOL_RTSP,
    TRANSPORT_PROTOCOL_HTTP,
)

STREAM_TYPE_RTP_UNICAST: Final[str] = "RTP-Unicast"
STREAM_TYPE_RTP_MULTICAST: Final[str] = "RTP-Multicast"
STREAM_TYPES: Sequence[str] = (STREAM_TYPE_RTP_UNICAST, STREAM_TYPE_RTP_MULTICAST)

PROFILE_TOKEN_MAX_LENGTH: Final[int] = 64
