# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional


@dataclass
class LoggingConfig:
    config_path: Optional[str] = None
    root_severity: Optional[str] = None
