# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class ContextConfig:
    auto_fixer: bool = True
    """
    Automatically fixes configuration files when known issues occur.
    """
