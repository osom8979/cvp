# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class LoggingConfig:
    config_path: str = ""
    root_severity: str = ""
