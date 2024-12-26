# -*- coding: utf-8 -*-

from typing import Final

CVP_HOME_DIRNAME: Final[str] = ".cvp"
CVP_YML_FILENAME: Final[str] = "cvp.yml"
GUI_INI_FILENAME: Final[str] = "gui.ini"
LOGGING_JSON_FILENAME: Final[str] = "logging.json"

DEFAULT_THEME: Final[str] = "dark"

DEFAULT_FONT_SCALE: Final[float] = 1.0
DEFAULT_NORMAL_TEXT_FONT_SIZE: Final[int] = 14
DEFAULT_MEDIUM_TEXT_FONT_SIZE: Final[int] = 18
DEFAULT_LARGE_TEXT_FONT_SIZE: Final[int] = 24
DEFAULT_NORMAL_ICON_FONT_SIZE: Final[int] = 14
DEFAULT_MEDIUM_ICON_FONT_SIZE: Final[int] = 18
DEFAULT_LARGE_ICON_FONT_SIZE: Final[int] = 24

CONFIG_VALUE_SEPARATOR: Final[str] = ","
CHECKSUM_DELIMITER: Final[str] = ":"

CODEPOINT_RANGES_EXTENSION: Final[str] = ".ranges"
CODEPOINT_GLYPHS_EXTENSION: Final[str] = ".glyphs"
KEYRING_EXTENSION: Final[str] = ".cfg"

LOCAL_DOTENV_FILENAME: Final[str] = ".env.local"

MAX_THREAD_WORKERS: Final[int] = 5
MAX_PROCESS_WORKERS: Final[int] = 5

THREAD_POOL_PREFIX: Final[str] = "cvp.threadpool"

DEFAULT_LOGGING_STEP: Final[int] = 1000
DEFAULT_SLOW_CALLBACK_DURATION: Final[float] = 0.05

MIN_SIDEBAR_WIDTH: Final[float] = 160.0
MAX_SIDEBAR_WIDTH: Final[float] = 260.0

MIN_SIDEBAR_HEIGHT: Final[float] = 160.0
MAX_SIDEBAR_HEIGHT: Final[float] = 260.0

MIN_WINDOW_WIDTH: Final[int] = 400
MIN_WINDOW_HEIGHT: Final[int] = 300

DEFAULT_API_SELECT_WIDTH: Final[float] = 180.0
MIN_API_SELECT_WIDTH: Final[float] = 100.0
MAX_API_SELECT_WIDTH: Final[float] = 300.0

MIN_POPUP_WIDTH: Final[int] = 120
MIN_POPUP_HEIGHT: Final[int] = 50
MIN_POPUP_CONFIRM_WIDTH: Final[int] = 280
MIN_POPUP_CONFIRM_HEIGHT: Final[int] = 80
MIN_POPUP_TEXT_INPUT_WIDTH: Final[int] = 200
MIN_POPUP_TEXT_INPUT_HEIGHT: Final[int] = 120
MIN_POPUP_OPEN_FILE_WIDTH: Final[int] = 480
MIN_POPUP_OPEN_FILE_HEIGHT: Final[int] = 380

AUI_PADDING_WIDTH: Final[float] = 8.0
AUI_PADDING_HEIGHT: Final[float] = 8.0

PROCESS_TEARDOWN_TIMEOUT: Final[float] = 2.0

STREAM_LOGGING_MAXSIZE: Final[int] = 65536
STREAM_LOGGING_NEWLINE_SIZE: Final[int] = 88

WSD_IPV4_MULTICAST_ADDRESS: Final[str] = "239.255.255.250"
WSD_IPV6_MULTICAST_ADDRESS: Final[str] = "ff02::c"
WSD_PORT_NUMBER: Final[int] = 3702
WSD_TIMEOUT: Final[float] = 30.0
WSD_NAME_DEFAULT: Final[str] = "New Device"

ZEEP_ELEMENT_SEPARATOR: Final[str] = "."

DEFAULT_CURVE_TESSELLATION_TOL: Final[float] = 1.25
"""
Tessellation tolerance when using BezierCurve without a specific number of segments.
Decrease for highly tessellated curves (higher quality, more polygons),
Increase to reduce quality.
"""
