# -*- coding: utf-8 -*-

from enum import StrEnum, unique
from typing import Any, Iterator, Optional, Protocol


@unique
class TransportProtocol(StrEnum):
    UDP = "UDP"
    TCP = "TCP"  # Deprecated
    RTSP = "RTSP"
    HTTP = "HTTP"


@unique
class StreamType(StrEnum):
    RTPUnicast = "RTP-Unicast"
    RTPMulticast = "RTP-Multicast"


@unique
class SetDateTimeType(StrEnum):
    Manual = "Manual"
    NTP = "NTP"


class GetDeviceInformationResponse(Protocol):
    Manufacturer: str
    Model: str
    FirmwareVersion: str
    SerialNumber: str
    HardwareId: str


class OnvifVersion(Protocol):
    Major: int
    Minor: int


class Service(Protocol):
    Namespace: str
    XAddr: str
    Capabilities: Optional[Any]
    Version: OnvifVersion


class GetServicesResponse(Protocol):
    def __iter__(self) -> Iterator[Service]: ...
    def __getitem__(self, index: int) -> Service: ...
    def __len__(self) -> int: ...


class TimeZone(Protocol):
    TZ: str


class SystemDateTime(Protocol):
    DateTimeType: SetDateTimeType
    DaylightSavings: bool
    TimeZone: Optional[TimeZone]


class Date(Protocol):
    Year: int
    Month: int
    """Range is 1 to 12."""
    Day: int
    """Range is 1 to 31."""


class Time(Protocol):
    Hour: int
    """Range is 0 to 23."""
    Minute: int
    """Range is 0 to 59."""
    Second: int
    """Range is 0 to 61(typically 59)."""


class DateTime(Protocol):
    Time: Time
    Date: Date


SystemDateTimeExtension = Any


class GetSystemDateAndTimeResponse(Protocol):
    SystemDateAndTime: SystemDateTime
    UTCDateTime: Optional[DateTime]
    LocalDateTime: Optional[DateTime]
    Extension: Optional[SystemDateTimeExtension]
