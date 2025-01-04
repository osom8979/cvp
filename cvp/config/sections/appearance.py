# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.variables import GUI_THEME


@dataclass
class AppearanceConfig:
    theme: str = GUI_THEME
