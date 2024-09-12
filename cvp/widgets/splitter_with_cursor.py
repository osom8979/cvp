# -*- coding: utf-8 -*-

from typing import Optional, Union

from pygame import SYSTEM_CURSOR_SIZENS, SYSTEM_CURSOR_SIZEWE
from pygame.cursors import Cursor
from pygame.mouse import get_cursor, set_cursor

from cvp.widgets.splitter import (
    AVAILABLE_REGION_SIZE,
    DEFAULT_SPLITTER_SIZE,
    DEFAULT_SPLITTER_THICKNESS,
    SplitterOrientation,
    splitter,
)


class SplitterWithCursor:
    _hovered_cursor: Optional[Cursor]

    def __init__(
        self,
        identifier: str,
        orientation: SplitterOrientation,
        width: float,
        height: float,
        flags=0,
        thickness=DEFAULT_SPLITTER_THICKNESS,
        cursor: Optional[Union[Cursor, int]] = None,
    ):
        self._identifier = identifier
        self._orientation = orientation
        self._width = width
        self._height = height
        self._flags = flags
        self._thickness = thickness

        self._hovered_cursor = None
        self._prev_cursor = Cursor()
        self._prev_hovered = False

        if cursor is not None:
            if isinstance(cursor, Cursor):
                self._hovered_cursor = cursor
            elif isinstance(cursor, int):
                self._hovered_cursor = Cursor(cursor)
            else:
                raise TypeError(f"Unsupported cursor type: {type(cursor).__name__}")

    @classmethod
    def from_vertical(
        cls,
        identifier: str,
        width=DEFAULT_SPLITTER_SIZE,
        height=AVAILABLE_REGION_SIZE,
        flags=0,
        thickness=DEFAULT_SPLITTER_THICKNESS,
        cursor: Optional[Union[Cursor, int]] = SYSTEM_CURSOR_SIZEWE,
    ):
        return cls(
            identifier=identifier,
            orientation=SplitterOrientation.vertical,
            width=width,
            height=height,
            flags=flags,
            thickness=thickness,
            cursor=cursor,
        )

    @classmethod
    def from_horizontal(
        cls,
        identifier: str,
        width=AVAILABLE_REGION_SIZE,
        height=DEFAULT_SPLITTER_SIZE,
        flags=0,
        thickness=DEFAULT_SPLITTER_THICKNESS,
        cursor: Optional[Union[Cursor, int]] = SYSTEM_CURSOR_SIZENS,
    ):
        return cls(
            identifier=identifier,
            orientation=SplitterOrientation.horizontal,
            width=width,
            height=height,
            flags=flags,
            thickness=thickness,
            cursor=cursor,
        )

    def do_process(self):
        result = splitter(
            self._identifier,
            self._orientation,
            self._width,
            self._height,
            self._flags,
            self._thickness,
        )

        try:
            if self._hovered_cursor is not None:
                if not self._prev_hovered and result.hovered:
                    self._prev_cursor = get_cursor()
                    set_cursor(self._hovered_cursor)
                    self._prev_hovered = True
                elif self._prev_hovered and not result.hovered and not result.changed:
                    set_cursor(self._prev_cursor)
                    self._prev_hovered = False
        finally:
            return result
