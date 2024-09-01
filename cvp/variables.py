# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Final

CVP_HOME_DIRNAME: Final[str] = ".cvp"
CVP_INI_FILENAME: Final[str] = "cvp.ini"
GUI_INI_FILENAME: Final[str] = "gui.ini"
LOGGING_JSON_FILENAME: Final[str] = "logging.json"

CONFIG_VALUE_SEPARATOR: Final[str] = ","

FONT_RANGES_EXTENSION: Final[str] = ".ranges"
MEDIA_SECTION_PREFIX: Final[str] = "media."

DEFAULT_CVP_HOME_PATH: Final[str] = str(Path.home() / CVP_HOME_DIRNAME)

MIN_WINDOW_WIDTH: Final[int] = 400
MIN_WINDOW_HEIGHT: Final[int] = 300

MIN_SIDEBAR_WIDTH: Final[int] = 160

MIN_POPUP_WIDTH: Final[int] = 480
MIN_POPUP_HEIGHT: Final[int] = 380

MIN_OPEN_FILE_POPUP_WIDTH: Final[int] = 480
MIN_OPEN_FILE_POPUP_HEIGHT: Final[int] = 380

MIN_OPEN_URL_POPUP_WIDTH: Final[int] = 400
MIN_OPEN_URL_POPUP_HEIGHT: Final[int] = 140

PROCESS_TEARDOWN_TIMEOUT: Final[float] = 2.0

STREAM_LOGGING_MAXSIZE: Final[int] = 65536
STREAM_LOGGING_NEWLINE_SIZE: Final[int] = 88
