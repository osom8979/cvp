# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from uuid import uuid4

from cvp.config.sections.bases.manager import ManagerWindowConfig


@dataclass
class OnvifConfig:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    address: str = field(default_factory=str)
    name: str = field(default_factory=str)


@dataclass
class OnvifManagerConfig(ManagerWindowConfig):
    pass
