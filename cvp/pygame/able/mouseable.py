# -*- coding: utf-8 -*-

from typing import Literal, Sequence

from pygame import mouse as pg_mouse
from pygame.cursors import Cursor
from pygame.surface import Surface

from cvp.pygame.types import SequenceProtocol


class Mouseable:
    @staticmethod
    def mouse_get_pressed(num_buttons: Literal[3, 5] = 3):
        if num_buttons == 3:
            return pg_mouse.get_pressed(num_buttons=3)
        elif num_buttons == 5:
            return pg_mouse.get_pressed(num_buttons=5)
        else:
            raise ValueError(f"Unexpected num buttons: {num_buttons}")

    @staticmethod
    def mouse_get_pos():
        return pg_mouse.get_pos()

    @staticmethod
    def mouse_get_rel():
        return pg_mouse.get_rel()

    @staticmethod
    def mouse_set_pos(pos: Sequence[float]):
        assert isinstance(pos, SequenceProtocol)
        return pg_mouse.set_pos(pos)

    @staticmethod
    def mouse_set_pos_coords(x: float, y: float):
        return pg_mouse.set_pos(x, y)

    @staticmethod
    def mouse_set_visible(value: bool):
        return pg_mouse.set_visible(value)

    @staticmethod
    def mouse_get_visible():
        return pg_mouse.get_visible()

    @staticmethod
    def mouse_get_focused():
        return pg_mouse.get_focused()

    @staticmethod
    def mouse_set_cursor(cursor: Cursor):
        return pg_mouse.set_cursor(cursor)

    @staticmethod
    def mouse_set_cursor_with_constant(constant: int):
        return pg_mouse.set_cursor(constant)

    @staticmethod
    def mouse_set_cursor_with_masks(
        size: Sequence[int],
        hotspot: Sequence[int],
        xor_masks: Sequence[int],
        and_masks: Sequence[int],
    ):
        assert isinstance(size, SequenceProtocol)
        assert isinstance(hotspot, SequenceProtocol)
        assert isinstance(xor_masks, SequenceProtocol)
        assert isinstance(and_masks, SequenceProtocol)
        return pg_mouse.set_cursor(size, hotspot, xor_masks, and_masks)

    @staticmethod
    def mouse_set_cursor_with_surface(hotspot: Sequence[int], surface: Surface):
        assert isinstance(hotspot, SequenceProtocol)
        return pg_mouse.set_cursor(hotspot, surface)

    @staticmethod
    def mouse_get_cursor():
        return pg_mouse.get_cursor()

    @staticmethod
    def mouse_get_relative_mode():
        return pg_mouse.get_relative_mode()

    @staticmethod
    def mouse_set_relative_mode(enable: bool):
        return pg_mouse.set_relative_mode(enable)
