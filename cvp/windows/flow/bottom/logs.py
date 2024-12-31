# -*- coding: utf-8 -*-

from collections import deque
from logging import Handler, LogRecord
from typing import Callable, Deque, Tuple
from weakref import finalize

import imgui

from cvp.context.context import Context
from cvp.flow.datas.graph import Graph
from cvp.imgui.begin_child import begin_child
from cvp.imgui.fonts.mapper import FontMapper
from cvp.logging.logging import flow_logger as logger
from cvp.types.override import override
from cvp.widgets.tab import TabItem
from cvp.windows.flow.cursor import FlowCursor


class LoggingHandler(Handler):
    def __init__(self, callback: Callable[[str, str], None]):
        super().__init__()
        self._callback = callback

    @override
    def emit(self, record: LogRecord):
        self._callback(record.levelname, self.format(record))


def unregister_handler(handler: LoggingHandler) -> None:
    logger.removeHandler(handler)


class LogsTab(TabItem[Graph]):
    _lines: Deque[Tuple[str, str]]

    def __init__(self, context: Context, fonts: FontMapper, cursor: FlowCursor):
        super().__init__(context, "Logs")
        self._fonts = fonts
        self._cursor = cursor
        self._auto_scroll = False
        self._lines = deque(maxlen=100)
        self._handler = LoggingHandler(self.on_logging)
        logger.addHandler(self._handler)
        self._finalizer = finalize(self, unregister_handler, self._handler)

    def on_logging(self, level: str, message: str) -> None:
        self._lines.append((level, message))

    @override
    def on_process(self) -> None:
        with begin_child("## Logging", border=False):

            for level, message in self._lines:
                imgui.text(f"[{level}] {message}")

            if self._auto_scroll:
                imgui.set_scroll_here_y(1.0)
