# -*- coding: utf-8 -*-

from copy import deepcopy
from os import PathLike
from typing import Optional, TypedDict, get_type_hints

from yaml import dump, full_load


class SerializedFlowGraph(TypedDict):
    name: str
    description: str


def get_serialized_hints():
    return get_type_hints(SerializedFlowGraph)


class FlowGraph:
    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        self.name = name if name else str()
        self.description = description if description else str()

    def __repr__(self):
        return (
            f"<{type(self).__name__} @{id(self)} "
            f"name='{self.name}' "
            f"description='{self.description}'>"
        )

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, type(self))
            and self.name == other.name
            and self.description == other.description
        )

    def __copy__(self):
        return type(self)(self.name)

    def __deepcopy__(self, memo):
        result = type(self)(deepcopy(self.name, memo))
        assert isinstance(memo, dict)
        memo[id(self)] = result
        return result

    def __serialize__(self):
        return SerializedFlowGraph(
            name=self.name,
            description=self.description,
        )

    def __deserialize__(self, data):
        assert isinstance(data, dict)
        for key, cls in get_serialized_hints().items():
            assert hasattr(self, key)
            setattr(self, key, data.get(key, cls()))

    def dumps_yaml(self, encoding="utf-8") -> bytes:
        return dump(self.__serialize__()).encode(encoding)

    def loads_yaml(self, data: bytes) -> None:
        self.__deserialize__(full_load(data))

    def read_yaml(self, file: PathLike[str]) -> None:
        with open(file, "rb") as f:
            self.loads_yaml(f.read())

    def write_yaml(self, file: PathLike[str]) -> None:
        with open(file, "wb") as f:
            f.write(self.dumps_yaml())
