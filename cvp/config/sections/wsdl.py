# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class WsdlConfig:
    no_cache: bool = False
