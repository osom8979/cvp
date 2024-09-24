# -*- coding: utf-8 -*-

from typing import Optional, Union

from pygame import SYSTEM_CURSOR_SIZENS, SYSTEM_CURSOR_SIZEWE
from pygame.cursors import Cursor
from pygame.mouse import get_cursor, set_cursor

from cvp.gui.splitter import (
    AVAILABLE_REGION_SIZE,
    DEFAULT_HORIZONTAL_SPLITTER_IDENTIFIER,
    DEFAULT_SPLITTER_SIZE,
    DEFAULT_SPLITTER_THICKNESS,
    DEFAULT_VERTICAL_SPLITTER_IDENTIFIER,
    SplitterOrientation,
    splitter,
)


class SplitterWithCursor:
    _hovered_cursor: Optional[Cursor]
    _prev_cursor: Optional[Cursor]

    def __init__(
        self,
        identifier: str,
        orientation: SplitterOrientation,
        width: float,
        height: float,
        min_value: Optional[Union[float, int]] = None,
        max_value: Optional[Union[float, int]] = None,
        flags=0,
        thickness=DEFAULT_SPLITTER_THICKNESS,
        cursor: Optional[Union[Cursor, int]] = None,
    ):
        self._identifier = identifier
        self._orientation = orientation
        self._width = width
        self._height = height
        self._min_value = min_value
        self._max_value = max_value
        self._flags = flags
        self._thickness = thickness

        self._hovered_cursor = None
        self._prev_cursor = None
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
        identifier=DEFAULT_VERTICAL_SPLITTER_IDENTIFIER,
        width=DEFAULT_SPLITTER_SIZE,
        height=AVAILABLE_REGION_SIZE,
        min_value: Optional[Union[float, int]] = None,
        max_value: Optional[Union[float, int]] = None,
        flags=0,
        thickness=DEFAULT_SPLITTER_THICKNESS,
        cursor: Optional[Union[Cursor, int]] = SYSTEM_CURSOR_SIZEWE,
    ):
        return cls(
            identifier=identifier,
            orientation=SplitterOrientation.vertical,
            width=width,
            height=height,
            min_value=min_value,
            max_value=max_value,
            flags=flags,
            thickness=thickness,
            cursor=cursor,
        )

    @classmethod
    def from_horizontal(
        cls,
        identifier=DEFAULT_HORIZONTAL_SPLITTER_IDENTIFIER,
        width=AVAILABLE_REGION_SIZE,
        height=DEFAULT_SPLITTER_SIZE,
        min_value: Optional[Union[float, int]] = None,
        max_value: Optional[Union[float, int]] = None,
        flags=0,
        thickness=DEFAULT_SPLITTER_THICKNESS,
        cursor: Optional[Union[Cursor, int]] = SYSTEM_CURSOR_SIZENS,
    ):
        return cls(
            identifier=identifier,
            orientation=SplitterOrientation.horizontal,
            width=width,
            height=height,
            min_value=min_value,
            max_value=max_value,
            flags=flags,
            thickness=thickness,
            cursor=cursor,
        )

    def change_hovered_cursor(self) -> None:
        if self._hovered_cursor is None:
            return

        self._prev_cursor = get_cursor()
        set_cursor(self._hovered_cursor)

    def change_prev_cursor(self) -> None:
        if self._prev_cursor is None:
            return

        set_cursor(self._prev_cursor)
        self._prev_cursor = None

    def do_splitter(self):
        return splitter(
            self._identifier,
            self._orientation,
            self._width,
            self._height,
            self._flags,
            self._thickness,
        )

    def do_process(self):
        result = self.do_splitter()

        if not self._prev_hovered and result.hovered:
            self.change_hovered_cursor()
            self._prev_hovered = True
        elif self._prev_hovered and not result.hovered and not result.changed:
            self.change_prev_cursor()
            self._prev_hovered = False

        return result
