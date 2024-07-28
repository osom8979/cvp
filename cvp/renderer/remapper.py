# -*- coding: utf-8 -*-

from typing import Dict

import pygame


class KeycodeRemapper:
    """
    We need to go to custom keycode since imgui only support keycode from 0..512 or -1
    """

    _pygame_to_imgui: Dict[int, int]

    def __init__(self):
        self._pygame_to_imgui = dict()
        self.l_ctrl = self._at(pygame.K_LCTRL)
        self.r_ctrl = self._at(pygame.K_RCTRL)
        self.l_alt = self._at(pygame.K_LALT)
        self.r_alt = self._at(pygame.K_RALT)
        self.l_shift = self._at(pygame.K_LSHIFT)
        self.r_shift = self._at(pygame.K_RSHIFT)
        self.l_super = self._at(pygame.K_LSUPER)
        self.r_super = self._at(pygame.K_RSUPER)

    def _at(self, pygame_keycode: int) -> int:
        if pygame_keycode not in self._pygame_to_imgui:
            self._pygame_to_imgui[pygame_keycode] = len(self._pygame_to_imgui)
        return self._pygame_to_imgui[pygame_keycode]

    def __call__(self, pygame_keycode: int) -> int:
        return self._at(pygame_keycode)
