# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Final, Tuple

"""
'%Y'
    Year with century as a decimal number.
    e.g. 0001, 0002, …, 2013, 2014, …, 9998, 9999
'%m'
    Month as a zero-padded decimal number.
    e.g. 01, 02, …, 12
'%d'
    Day of the month as a zero-padded decimal number.
    e.g. 01, 02, …, 31
"""
DATENAME_LONG_FORMAT: Final[str] = "%Y-%m-%d"  # e.g. '2022-02-14'
DATENAME_SHORT_FORMAT: Final[str] = "%Y%m%d"

"""
"%H'
    Hour (24-hour clock) as a zero-padded decimal number.
    e.g. 00, 01, …, 23
'%M'
    Minute as a zero-padded decimal number.
    e.g. 00, 01, …, 59
'%S'
    Second as a zero-padded decimal number.
    e.g. 00, 01, …, 59
'%f'
    Microsecond as a decimal number, zero-padded to 6 digits.
    e.g. 000000, 000001, …, 999999
"""
TIMENAME_LONG_FORMAT: Final[str] = "%H_%M_%S.%f"  # e.g. '14_28_19.286335'
TIMENAME_SHORT_FORMAT: Final[str] = "%H%M%S"

DATETIME_LONG_FORMAT: Final[str] = f"{DATENAME_LONG_FORMAT}T{TIMENAME_LONG_FORMAT}"
DATETIME_SHORT_FORMAT: Final[str] = f"{DATENAME_SHORT_FORMAT}-{TIMENAME_SHORT_FORMAT}"


def long_datename_and_timename(date_time: datetime) -> Tuple[str, str]:
    directory = date_time.strftime(DATENAME_LONG_FORMAT)
    filename = date_time.strftime(TIMENAME_LONG_FORMAT)
    return directory, filename


def short_datename_and_timename(date_time: datetime) -> Tuple[str, str]:
    directory = date_time.strftime(DATENAME_SHORT_FORMAT)
    filename = date_time.strftime(TIMENAME_SHORT_FORMAT)
    return directory, filename


def long_datetime_name(date_time: datetime) -> str:
    return date_time.strftime(DATETIME_LONG_FORMAT)


def short_datetime_name(date_time: datetime) -> str:
    return date_time.strftime(DATETIME_SHORT_FORMAT)
