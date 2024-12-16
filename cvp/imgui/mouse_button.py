# -*- coding: utf-8 -*-

from enum import Enum, auto, unique
from typing import Optional

from cvp.patterns.delta import Delta
from cvp.types.shapes import Point


@unique
class ButtonState(Enum):
    normal = auto()
    ready = auto()
    dragging = auto()


class MouseButton:
    _pivot: Optional[Point]

    def __init__(self) -> None:
        self._down = Delta.from_single_value(False)
        self._dragging = Delta.from_single_value(False)
        self._state = ButtonState.normal
        self._pivot = None

    @property
    def pivot(self):
        return self._pivot

    @property
    def is_down(self) -> bool:
        return self._down.value

    @property
    def is_up(self) -> bool:
        return not self._down.value

    @property
    def changed_down(self) -> bool:
        return self._down.changed and self._down.value

    @property
    def changed_up(self) -> bool:
        return self._down.changed and not self._down.value

    @property
    def is_dragging(self) -> bool:
        return self._dragging.value

    @property
    def start_dragging(self) -> bool:
        return self._dragging.changed and self._dragging.value

    @property
    def end_dragging(self) -> bool:
        return self._dragging.changed and not self._dragging.value

    def update(self, down: bool, mouse_point: Point) -> None:
        if self._down.update(down):
            if self._down.value:
                self._state = ButtonState.ready
                self._pivot = mouse_point
            else:
                self._state = ButtonState.normal
                self._pivot = None

        if not self._down.value:
            assert self._state == ButtonState.normal
            assert self._pivot is None
            self._dragging.update(False)
            return

        assert self._state != ButtonState.normal
        assert self._pivot is not None

        if self._state == ButtonState.ready and self._pivot != mouse_point:
            self._state = ButtonState.dragging

        self._dragging.update(self._state == ButtonState.dragging)
