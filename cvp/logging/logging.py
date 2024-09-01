# -*- coding: utf-8 -*-

from json import dumps
from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    FATAL,
    INFO,
    NOTSET,
    WARN,
    WARNING,
    Formatter,
    StreamHandler,
)
from logging import config as logging_config
from logging import getLogger
from logging.handlers import TimedRotatingFileHandler
from os import PathLike
from sys import stdout
from typing import Optional, Union

from cvp.logging.defaults import (
    CVP_LOGGER_NAME,
    DEFAULT_DATEFMT,
    DEFAULT_FORMAT,
    DEFAULT_LOGGING_CONFIG,
    DEFAULT_SIMPLE_LOGGING_FORMAT,
    DEFAULT_SIMPLE_LOGGING_STYLE,
    DEFAULT_STYLE,
    DEFAULT_TIMED_ROTATING_WHEN,
    MPV_LOGGER_NAME,
    TimedRotatingWhenLiteral,
)
from cvp.system.environ_keys import CVP_HOME

logger = getLogger(CVP_LOGGER_NAME)
mpv_logger = getLogger(MPV_LOGGER_NAME)

SEVERITY_NAME_CRITICAL = "critical"
SEVERITY_NAME_FATAL = "fatal"
SEVERITY_NAME_ERROR = "error"
SEVERITY_NAME_WARNING = "warning"
SEVERITY_NAME_WARN = "warn"
SEVERITY_NAME_INFO = "info"
SEVERITY_NAME_DEBUG = "debug"
SEVERITY_NAME_NOTSET = "notset"
SEVERITY_NAME_OFF = "off"

SEVERITIES = (
    SEVERITY_NAME_CRITICAL,
    SEVERITY_NAME_FATAL,
    SEVERITY_NAME_ERROR,
    SEVERITY_NAME_WARNING,
    SEVERITY_NAME_WARN,
    SEVERITY_NAME_INFO,
    SEVERITY_NAME_DEBUG,
    SEVERITY_NAME_NOTSET,
    SEVERITY_NAME_OFF,
)


def convert_level_number(level: Optional[Union[str, int]] = None) -> int:
    if level is None:
        return DEBUG

    if isinstance(level, str):
        ll = level.lower()
        if ll == SEVERITY_NAME_CRITICAL:
            return CRITICAL
        elif ll == SEVERITY_NAME_FATAL:
            return FATAL
        elif ll == SEVERITY_NAME_ERROR:
            return ERROR
        elif ll == SEVERITY_NAME_WARNING:
            return WARNING
        elif ll == SEVERITY_NAME_WARN:
            return WARN
        elif ll == SEVERITY_NAME_INFO:
            return INFO
        elif ll == SEVERITY_NAME_DEBUG:
            return DEBUG
        elif ll == SEVERITY_NAME_NOTSET:
            return NOTSET
        elif ll == SEVERITY_NAME_OFF:
            return CRITICAL + 100
        else:
            try:
                return int(ll)
            except ValueError:
                raise ValueError(f"Unknown level: {level}")
    elif isinstance(level, int):
        return level
    else:
        raise TypeError(f"Unsupported level type: {type(level)}")


def convert_printable_level(level: Union[str, int]) -> str:
    if isinstance(level, str):
        return level
    if isinstance(level, int):
        if level > CRITICAL:
            return "OverCritical"
        if level == CRITICAL:
            return "Critical"
        if level > ERROR:
            return "OverError"
        if level == ERROR:
            return "Error"
        if level > WARNING:
            return "OverWarning"
        if level == WARNING:
            return "Warning"
        if level > INFO:
            return "OverInfo"
        if level == INFO:
            return "Info"
        if level > DEBUG:
            return "OverDebug"
        if level == DEBUG:
            return "Debug"
        if level > NOTSET:
            return "OverNotSet"
        if level == NOTSET:
            return "NotSet"
    return str(level)


def set_root_level(level: Union[str, int]) -> None:
    getLogger().setLevel(convert_level_number(level))


def set_default_logging_config() -> None:
    logging_config.dictConfig(DEFAULT_LOGGING_CONFIG)


def dumps_default_logging_config(cvp_home: Union[str, PathLike[str]]) -> str:
    json = dumps(DEFAULT_LOGGING_CONFIG, indent=4)
    return json.replace(f"${{{CVP_HOME}}}", str(cvp_home))


def add_default_rotate_file_logging(
    prefix: str,
    when: Union[str, TimedRotatingWhenLiteral] = DEFAULT_TIMED_ROTATING_WHEN,
    level=DEBUG,
) -> None:
    formatter = Formatter(
        fmt=DEFAULT_FORMAT,
        datefmt=DEFAULT_DATEFMT,
        style=DEFAULT_STYLE,
    )

    handler = TimedRotatingFileHandler(prefix, when)
    handler.suffix = "%Y%m%d_%H%M%S.log"
    handler.setFormatter(formatter)
    handler.setLevel(level)

    getLogger().addHandler(handler)


def add_default_colored_logging(level=DEBUG) -> None:
    from cvp.logging.formatters.colored import ColoredFormatter

    formatter = ColoredFormatter(
        fmt=DEFAULT_FORMAT,
        datefmt=DEFAULT_DATEFMT,
        style=DEFAULT_STYLE,
    )

    handler = StreamHandler(stdout)
    handler.setFormatter(formatter)
    handler.setLevel(level)

    getLogger().addHandler(handler)


def add_default_logging(level=DEBUG) -> None:
    formatter = Formatter(
        fmt=DEFAULT_FORMAT,
        datefmt=DEFAULT_DATEFMT,
        style=DEFAULT_STYLE,
    )

    handler = StreamHandler(stdout)
    handler.setFormatter(formatter)
    handler.setLevel(level)

    getLogger().addHandler(handler)


def add_simple_logging(level=DEBUG) -> None:
    formatter = Formatter(
        fmt=DEFAULT_SIMPLE_LOGGING_FORMAT,
        style=DEFAULT_SIMPLE_LOGGING_STYLE,
    )

    handler = StreamHandler(stdout)
    handler.setFormatter(formatter)
    handler.setLevel(level)

    getLogger().addHandler(handler)
