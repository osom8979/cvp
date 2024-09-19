# -*- coding: utf-8 -*-

from typing import NamedTuple

import imgui


class CheckboxResult(NamedTuple):
    clicked: bool
    state: bool

    def __bool__(self):
        return self.clicked


def checkbox(label: str, state: bool):
    clicked, state = imgui.checkbox(label, state)
    assert isinstance(clicked, bool)
    assert isinstance(state, bool)
    return CheckboxResult(clicked, state)
