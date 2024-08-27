# -*- coding: utf-8 -*-

import sys
from functools import lru_cache


@lru_cache
def default_creation_flags() -> int:
    if sys.platform == "win32":
        from subprocess import CREATE_NO_WINDOW

        return CREATE_NO_WINDOW
    else:
        return 0
