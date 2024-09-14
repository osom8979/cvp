# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Final

VERBOSE_LEVEL_0: Final[int] = 0
VERBOSE_LEVEL_1: Final[int] = 1
VERBOSE_LEVEL_2: Final[int] = 2

CVP_HOME_DIRNAME: Final[str] = ".cvp"
CVP_INI_FILENAME: Final[str] = "cvp.ini"
GUI_INI_FILENAME: Final[str] = "gui.ini"
LOGGING_JSON_FILENAME: Final[str] = "logging.json"

DEFAULT_CVP_HOME_PATH: Final[str] = str(Path.home() / CVP_HOME_DIRNAME)

CONFIG_VALUE_SEPARATOR: Final[str] = ","
CHECKSUM_DELIMITER: Final[str] = ":"

FONT_RANGES_EXTENSION: Final[str] = ".ranges"

FLOW_SECTION_PREFIX: Final[str] = "flow."
LAYOUT_SECTION_PREFIX: Final[str] = "layout."
MEDIA_SECTION_PREFIX: Final[str] = "media."

LOCAL_DOTENV_FILENAME: Final[str] = ".env.local"

MAX_THREAD_WORKERS: Final[int] = 5
MAX_PROCESS_WORKERS: Final[int] = 5

THREAD_POOL_PREFIX: Final[str] = "cvp.threadpool"

DEFAULT_LOGGING_STEP: Final[int] = 1000
DEFAULT_SLOW_CALLBACK_DURATION: Final[float] = 0.05

MIN_WINDOW_WIDTH: Final[int] = 400
MIN_WINDOW_HEIGHT: Final[int] = 300

MIN_SIDEBAR_WIDTH: Final[int] = 160

MIN_POPUP_WIDTH: Final[int] = 120
MIN_POPUP_HEIGHT: Final[int] = 50
MIN_POPUP_CONFIRM_WIDTH: Final[int] = 280
MIN_POPUP_CONFIRM_HEIGHT: Final[int] = 80
MIN_POPUP_TEXT_INPUT_WIDTH: Final[int] = 200
MIN_POPUP_TEXT_INPUT_HEIGHT: Final[int] = 120

MIN_OPEN_FILE_POPUP_WIDTH: Final[int] = 480
MIN_OPEN_FILE_POPUP_HEIGHT: Final[int] = 380

MIN_OPEN_URL_POPUP_WIDTH: Final[int] = 400
MIN_OPEN_URL_POPUP_HEIGHT: Final[int] = 140

PROCESS_TEARDOWN_TIMEOUT: Final[float] = 2.0

STREAM_LOGGING_MAXSIZE: Final[int] = 65536
STREAM_LOGGING_NEWLINE_SIZE: Final[int] = 88
