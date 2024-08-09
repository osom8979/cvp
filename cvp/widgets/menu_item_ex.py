# -*- coding: utf-8 -*-

from typing import Optional

import imgui


class MenuItemResult:
    def __init__(self, result):
        assert isinstance(result, tuple)
        assert 2 == len(result)
        self.clicked = result[0]
        self.state = result[1]

    def __bool__(self):
        return self.clicked


def menu_item_ex(
    label: str,
    selected=False,
    shortcut: Optional[str] = None,
    enabled=True,
):
    return MenuItemResult(imgui.menu_item(label, shortcut, selected, enabled))
