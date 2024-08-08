# -*- coding: utf-8 -*-

from typing import Optional

from cvp.config.config import Config


class EmptyConfig(Config):
    def __init__(self, cvp_home: Optional[str] = None):
        super().__init__(filename=None, cvp_home=cvp_home)
