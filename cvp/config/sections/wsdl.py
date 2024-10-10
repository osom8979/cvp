# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class WsdlConfig:
    no_verify: bool = False
    no_cache: bool = False
