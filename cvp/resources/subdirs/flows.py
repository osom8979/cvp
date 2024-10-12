# -*- coding: utf-8 -*-

import os
from os import PathLike
from pathlib import Path
from typing import Union

from cvp.system.path import PathFlavour


class Flows(PathFlavour):
    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path)

    def find_graph_files(self):
        result = list()
        for dirpath, dirnames, filenames in os.walk(self):
            for filename in filenames:
                extension = os.path.splitext(filename)[1].lower()
                if extension in (".yml", ".yaml"):
                    result.append(Path(os.path.join(dirpath, filename)))
        return result

    def graph_filepath(self, uuid: str):
        return Path(self / f"{uuid}.yml")

    def has_graph(self, key: str) -> bool:
        return self.graph_filepath(key).exists()

    def save_graph(self, key: str, data: bytes) -> None:
        self.graph_filepath(key).write_bytes(data)

    def load_graph(self, key: str) -> bytes:
        return self.graph_filepath(key).read_bytes()

    def remove_graph(self, key: str) -> None:
        os.remove(self.graph_filepath(key))
