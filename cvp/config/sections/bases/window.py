# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class WindowConfig:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    title: str = field(default_factory=str)
    opened: bool = False
