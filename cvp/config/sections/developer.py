# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class DeveloperConfig:
    debug: bool = False
    verbose: int = 0
    metrics: bool = False
    style: bool = False
    demo: bool = False
