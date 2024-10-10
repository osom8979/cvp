# -*- coding: utf-8 -*-

import os
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from zeep.cache import Base as ZeepCacheBase

from cvp.logging.logging import wsdl_logger as logger
from cvp.types import override


class ZeepFileCache(ZeepCacheBase):
    def __init__(self, prefix: str):
        super().__init__()
        self._prefix = prefix

    def get_cache_path(self, url: str) -> Path:
        o = urlparse(url)
        hostname = o.hostname if o.hostname else "__unknown_host__"
        return Path(os.path.join(self._prefix, hostname, *o.path.split("/")))

    @override
    def add(self, url: str, content: Any):
        filepath = self.get_cache_path(url)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        try:
            if not filepath.exists():
                with filepath.open("wb") as f:
                    f.write(content)
        except BaseException as e:  # noqa
            logger.error(f"{type(self).__name__}.add(url={url}) error: {e}")
        else:
            logger.debug(f"{type(self).__name__}.add(url={url}) ok")

    @override
    def get(self, url: str):
        filepath = self.get_cache_path(url)
        try:
            if filepath.is_file():
                with filepath.open("rb") as f:
                    return f.read()
        except BaseException as e:  # noqa
            logger.error(f"{type(self).__name__}.get(url={url}) error: {e}")
        else:
            logger.debug(f"{type(self).__name__}.get(url={url}) ok")
        return None
