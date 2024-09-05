# -*- coding: utf-8 -*-

from typing import Any, Dict, Final, Literal, Sequence, get_args

from cvp.system.environ_keys import CVP_HOME

CVP_LOGGER_NAME: Final[str] = "cvp"

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

_simple_formatter = {
    "format": SIMPLE_FORMAT,
    "datefmt": SIMPLE_DATEFMT,
    "style": SIMPLE_STYLE,
}

_stdout_default = {
    "class": "logging.StreamHandler",
    "level": "DEBUG",
    "formatter": "default",
    "stream": "ext://sys.stdout",
}

_stdout_simple = {
    "class": "logging.StreamHandler",
    "level": "DEBUG",
    "formatter": "simple",
    "stream": "ext://sys.stdout",
}

_file_default = {
    "class": "logging.FileHandler",
    "level": "DEBUG",
    "formatter": "default",
    "filename": "cvp.log",
    "mode": "a",
    "encoding": "utf-8",
    "delay": False,
}

_rotating_file_default = {
    "class": "logging.handlers.RotatingFileHandler",
    "level": "DEBUG",
    "formatter": "default",
    "filename": f"${{{CVP_HOME}}}/logs/cvp_rotating",
    "mode": "a",
    "maxBytes": 10 * 1024 * 1024,
    "backupCount": 10,
    "encoding": "utf-8",
    "delay": False,
}

DEFAULT_LOGGING_CONFIG: Final[Dict[str, Any]] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": DEFAULT_FORMAT,
            "datefmt": DEFAULT_DATEFMT,
            "style": DEFAULT_STYLE,
        },
        "colored": {
            "class": "cvp.logging.formatters.colored.ColoredFormatter",
            "format": DEFAULT_FORMAT,
            "datefmt": DEFAULT_DATEFMT,
            "style": DEFAULT_STYLE,
        },
    },
    "handlers": {
        "stdout_colored": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "colored",
            "stream": "ext://sys.stdout",
        },
        "timed_rotating_file_default": {
            "class": "cvp.logging.handlers.file.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "default",
            "filename": f"${{{CVP_HOME}}}/logs/cvp_timed_rotating",
            "when": "D",
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
            "handlers": ["stdout_colored"],
            "level": "DEBUG",
        },
        CVP_LOGGER_NAME: {
            "handlers": ["timed_rotating_file_default"],
            "level": "DEBUG",
        },
    },
}
