# -*- coding: utf-8 -*-

import os
from abc import ABC, abstractmethod
from os import PathLike
from pathlib import Path
from typing import Any, Optional, Union

from cvp.system.path import PathFlavour
from cvp.types.override import override


class FormatInterface(ABC):
    @abstractmethod
    def dumps(self, data: Any) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def loads(self, data: bytes) -> Any:
        raise NotImplementedError


class BaseFormatPath(PathFlavour, FormatInterface):
    def __init__(self, path: Union[str, PathLike[str]], suffix: Optional[str] = None):
        super().__init__(path)
        self._suffix = suffix if suffix else str()

    @override
    def dumps(self, data: Any) -> bytes:
        raise NotImplementedError

    @override
    def loads(self, data: bytes) -> Any:
        raise NotImplementedError

    def object_path(self, *paths: str):
        if not paths:
            raise ValueError("At least one path must be specified")
        return Path(os.path.join(self, *paths) + self._suffix)

    def has_object(self, *paths: str) -> bool:
        return self.object_path(*paths).is_file()

    def read_object(self, *paths: str) -> Any:
        obj_path = self.object_path(*paths)
        obj_data = obj_path.read_bytes()
        return self.loads(obj_data)

    def write_object(self, o: Any, *paths: str) -> int:
        obj_path = self.object_path(*paths)
        obj_path.parent.mkdir(parents=True, exist_ok=True)
        obj_data = self.dumps(o)
        return obj_path.write_bytes(obj_data)

    def remove_object(self, *paths: str) -> None:
        return os.remove(self.object_path(*paths))
