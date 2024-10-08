# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.variables import DEFAULT_THEME


@dataclass
class AppearanceConfig:
    theme: str = DEFAULT_THEME
