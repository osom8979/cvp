# -*- coding: utf-8 -*-

from cvp.config.root import Config


class EmptyConfig(Config):
    def __init__(self):
        super().__init__(filename=None)
