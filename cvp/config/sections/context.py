# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class ContextConfig:
    auto_fixer: bool = True
