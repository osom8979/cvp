# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from typing import Union

import imgui


@unique
class Styles(StrEnum):
    dark = auto()
    light = auto()
    classic = auto()


def style_colors(style: Styles) -> None:
    if style == Styles.dark:
        imgui.style_colors_dark()
    elif style == Styles.light:
        imgui.style_colors_light()
    elif style == Styles.classic:
        imgui.style_colors_classic()
    else:
        raise ValueError(f"Unknown style: {style}")


def default_style_colors(style: Union[str, Styles], default=Styles.dark) -> None:
    try:
        style_colors(style if isinstance(style, Styles) else Styles(style))
    except:  # noqa
        style_colors(default)