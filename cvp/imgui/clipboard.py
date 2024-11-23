# -*- coding: utf-8 -*-

import imgui
import pygame


def put_clipboard_text(text: str) -> None:
    pygame.scrap.put_text(text)
    imgui.set_clipboard_text(text)


def get_clipboard_text() -> str:
    if result := pygame.scrap.get_text():
        return result

    if result := imgui.get_clipboard_text():
        return result

    return str()
