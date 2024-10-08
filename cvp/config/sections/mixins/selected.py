# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class SelectedMixin:
    selected: str = str()
