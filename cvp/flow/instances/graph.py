# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from os import PathLike
from typing import Optional

from yaml import dump, full_load

from cvp.flow.templates.graph import FlowGraph


@unique
class GraphKeys(StrEnum):
    name_ = auto()
    template = auto()


class Graph:
    __template_class__ = FlowGraph
    __keys__ = GraphKeys

    def __init__(
        self,
        name: Optional[str] = None,
        template: Optional[str] = None,
    ):
        self.name = name if name else str()
        self.template = template if template else str()

    def __repr__(self):
        return (
            f"<{type(self).__name__} @{id(self)}"
            f" name='{self.name}'"
            f" template='{self.template}'"
            ">"
        )

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, type(self))
            and self.name == other.name
            and self.template == other.template
        )

    def __copy__(self):
        return type(self)(
            name=copy(self.name),
            template=copy(self.template),
        )

    def __deepcopy__(self, memo):
        result = type(self)(
            name=deepcopy(self.name, memo),
            template=deepcopy(self.template, memo),
        )
        assert isinstance(memo, dict)
        memo[id(self)] = result
        return result

    def __serialize__(self):
        result = dict()
        result[self.__keys__.name_] = str(self.name)
        result[self.__keys__.template] = str(self.template)
        return result

    def __deserialize__(self, data):
        assert isinstance(data, dict)
        self.name = str(data.get(self.__keys__.name_, str()))
        self.template = str(data.get(self.__keys__.template, str()))

    def dumps_yaml(self, encoding="utf-8") -> bytes:
        return dump(self.__serialize__()).encode(encoding)

    def loads_yaml(self, data: bytes) -> None:
        self.__deserialize__(full_load(data))

    def write_yaml(self, file: PathLike[str], encoding="utf-8") -> None:
        with open(file, "wb") as f:
            f.write(self.dumps_yaml(encoding))

    def read_yaml(self, file: PathLike[str]) -> None:
        with open(file, "rb") as f:
            self.loads_yaml(f.read())
