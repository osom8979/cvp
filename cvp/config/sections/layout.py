# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from uuid import uuid4

from cvp.config.sections.bases.manager import ManagerWindowConfig


@dataclass
class LayoutConfig:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default_factory=str)


@dataclass
class LayoutManagerConfig(ManagerWindowConfig):
    pass
