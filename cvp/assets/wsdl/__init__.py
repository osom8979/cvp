# -*- coding: utf-8 -*-

import os
from functools import lru_cache

from cvp.assets import get_assets_dir


@lru_cache
def get_wsdl_dir() -> str:
    return os.path.join(get_assets_dir(), "wsdl")
