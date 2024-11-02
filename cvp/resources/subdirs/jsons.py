# -*- coding: utf-8 -*-

import os
from os import PathLike
from pathlib import Path
from typing import Any, Union

import orjson

from cvp.system.path import PathFlavour


class Jsons(PathFlavour):
    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path)

    @staticmethod
    def dumps(data: Any) -> bytes:
        return orjson.dumps(data)

    @staticmethod
    def loads(data: Union[bytes, bytearray, memoryview, str]) -> Any:
        return orjson.loads(data)

    def json_path(self, *paths: str):
        if not paths:
            raise ValueError("At least one path must be specified.")
        return Path(os.path.join(self, *paths))

    def has_json(self, *paths: str) -> bool:
        return self.json_path(*paths).is_file()

    def read_json(self, *paths: str) -> Any:
        obj_path = self.json_path(*paths)
        obj_data = obj_path.read_bytes()
        return self.loads(obj_data)

    def write_json(self, o: Any, *paths: str) -> int:
        obj_path = self.json_path(*paths)
        obj_path.parent.mkdir(parents=True, exist_ok=True)
        obj_data = self.dumps(o)
        return obj_path.write_bytes(obj_data)

    def remove_json(self, *paths: str) -> None:
        return os.remove(self.json_path(*paths))
