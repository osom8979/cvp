# -*- coding: utf-8 -*-

from os import PathLike
from pathlib import Path
from pickle import dumps, loads
from typing import Any, Final, Union

from cvp.system.path import PathFlavour

PICKLE_PROTOCOL_VERSION: Final[int] = 5
PICKLE_ENCODING: Final[str] = "ASCII"
PICKLE_SUFFIX: Final[str] = ".pickle"


class Onvifs(PathFlavour):
    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path)
        self._pickle_protocol_version = PICKLE_PROTOCOL_VERSION
        self._pickle_encoding = PICKLE_ENCODING
        self._pickle_suffix = PICKLE_SUFFIX

    def pickling(self, data: Any) -> bytes:
        return dumps(data, protocol=self._pickle_protocol_version)

    def unpickling(self, data: bytes) -> Any:
        return loads(data, encoding=self._pickle_encoding)

    def onvif_object_path(self, uuid: str, binding: str, api: str):
        return Path(self / uuid / binding / f"{api}{self._pickle_suffix}")

    def has_onvif_object(self, uuid: str, binding: str, api: str) -> bool:
        return self.onvif_object_path(uuid, binding, api).is_file()

    def read_onvif_object(self, uuid: str, binding: str, api: str) -> Any:
        json_path = self.onvif_object_path(uuid, binding, api)
        return self.unpickling(json_path.read_bytes())

    def write_onvif_object(self, uuid: str, binding: str, api: str, o: Any) -> int:
        json_path = self.onvif_object_path(uuid, binding, api)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        return json_path.write_bytes(self.pickling(o))
