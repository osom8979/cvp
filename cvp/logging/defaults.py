# -*- coding: utf-8 -*-

from typing import Final, Literal, Sequence, get_args

CVP_LOGGER_NAME: Final[str] = "cvp"
MPV_LOGGER_NAME: Final[str] = f"{CVP_LOGGER_NAME}.mpv"

TimedRotatingWhenLiteral = Literal[
    "S", "M", "H", "D", "W0", "W1", "W2", "W3", "W4", "W5", "W6", "midnight"
]  # W0=Monday
LoggingStyleLiteral = Literal["%", "{", "$"]

TIMED_ROTATING_WHEN: Final[Sequence[str]] = get_args(TimedRotatingWhenLiteral)
DEFAULT_TIMED_ROTATING_WHEN: Final[str] = "D"

DEFAULT_SIMPLE_LOGGING_FORMAT: Final[str] = "{levelname[0]} [{name}] {message}"
DEFAULT_SIMPLE_LOGGING_STYLE: Final[LoggingStyleLiteral] = "{"

FMT_TIME: Final[str] = "%(asctime)s.%(msecs)03d"
FMT_THREAD: Final[str] = "%(process)d/%(thread)s"

DEFAULT_FORMAT = f"{FMT_TIME} {FMT_THREAD} %(name)s %(levelname)s %(message)s"
DEFAULT_DATEFMT: Final[str] = "%Y-%m-%d %H:%M:%S"
DEFAULT_STYLE: Final[LoggingStyleLiteral] = "%"

SIMPLE_FORMAT: Final[str] = "{levelname[0]} {asctime} {name} {message}"
SIMPLE_DATEFMT: Final[str] = "%Y%m%d %H%M%S"
SIMPLE_STYLE: Final[LoggingStyleLiteral] = "{"

DEFAULT_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": DEFAULT_FORMAT,
            "datefmt": DEFAULT_DATEFMT,
            "style": DEFAULT_STYLE,
        },
        "simple": {
            "format": SIMPLE_FORMAT,
            "datefmt": SIMPLE_DATEFMT,
            "style": SIMPLE_STYLE,
        },
        "color": {
            "class": "cvp.logging.formatters.colored.ColoredFormatter",
            "format": DEFAULT_FORMAT,
            "datefmt": DEFAULT_DATEFMT,
            "style": DEFAULT_STYLE,
        },
    },
    "handlers": {
        "console_default": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "console_simple": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "console_color": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "color",
            "stream": "ext://sys.stdout",
        },
        "file_default": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "default",
            "filename": "cvp.log",
            "mode": "a",
            "encoding": "utf-8",
            "delay": False,
        },
        "file_rotate": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "default",
            "filename": "~/.cvp/logs/cvp.log",
            "mode": "a",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 10,
            "encoding": "utf-8",
            "delay": False,
        },
        "file_timed_rotate": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "default",
            "filename": "~/.cvp/logs/cvp",
            "when": DEFAULT_TIMED_ROTATING_WHEN,
            "interval": 1,
            "backupCount": 10,
            "encoding": "utf-8",
            "delay": False,
            "utc": False,
            "suffix": "%Y%m%d_%H%M%S.log",
        },
    },
    "loggers": {
        # root logger
        "": {
            "handlers": ["console_color"],
            "level": "DEBUG",
        },
        CVP_LOGGER_NAME: {
            "handlers": ["console_color"],
            "level": "DEBUG",
        },
        MPV_LOGGER_NAME: {
            "handlers": ["console_color"],
            "level": "DEBUG",
        },
    },
}
