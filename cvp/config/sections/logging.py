# -*- coding: utf-8 -*-

from dataclasses import dataclass, field


@dataclass
class LoggingConfig:
    config_path: str = field(default_factory=str)
    root_severity: str = field(default_factory=str)
