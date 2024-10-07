# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from os import PathLike
from typing import Iterable, List, Optional

from type_serialize import deserialize, serialize
from yaml import dump, full_load

from cvp.flow.templates.arc import FlowArc
from cvp.flow.templates.node import FlowNode


@unique
class FlowGraphKeys(StrEnum):
    class_name = auto()
    class_docs = auto()
    class_icon = auto()
    class_color = auto()
    class_nodes = auto()
    class_arcs = auto()


class FlowGraph:
    __keys__ = FlowGraphKeys

    def __init__(
        self,
        class_name: Optional[str] = None,
        class_docs: Optional[str] = None,
        class_icon: Optional[str] = None,
        class_color: Optional[str] = None,
        class_nodes: Optional[Iterable[FlowNode]] = None,
        class_arcs: Optional[Iterable[FlowArc]] = None,
    ):
        self.class_name = class_name if class_name else str()
        self.class_docs = class_docs if class_docs else str()
        self.class_icon = class_icon if class_icon else str()
        self.class_color = class_color if class_color else str()
        self.class_nodes = list(class_nodes if class_nodes else ())
        self.class_arcs = list(class_arcs if class_arcs else ())

    def __repr__(self):
        return (
            f"<{type(self).__name__} @{id(self)}"
            f" class_name='{self.class_name}'"
            f" class_docs='{self.class_docs}'"
            f" class_icon='{self.class_icon}'"
            f" class_color='{self.class_color}'"
            f" class_nodes={len(self.class_nodes)}"
            f" class_arcs={len(self.class_arcs)}>"
        )

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, type(self))
            and self.class_name == other.class_name
            and self.class_docs == other.class_docs
            and self.class_icon == other.class_icon
            and self.class_color == other.class_color
            and self.class_nodes == other.class_nodes
            and self.class_arcs == other.class_arcs
        )

    def __copy__(self):
        return type(self)(
            class_name=copy(self.class_name),
            class_docs=copy(self.class_docs),
            class_icon=copy(self.class_icon),
            class_color=copy(self.class_color),
            class_nodes=copy(self.class_nodes),
            class_arcs=copy(self.class_arcs),
        )

    def __deepcopy__(self, memo):
        result = type(self)(
            class_name=deepcopy(self.class_name, memo),
            class_docs=deepcopy(self.class_docs, memo),
            class_icon=deepcopy(self.class_icon, memo),
            class_color=deepcopy(self.class_color, memo),
            class_nodes=deepcopy(self.class_nodes, memo),
            class_arcs=deepcopy(self.class_arcs, memo),
        )
        assert isinstance(memo, dict)
        memo[id(self)] = result
        return result

    def __serialize__(self):
        result = dict()
        result[self.__keys__.class_name] = str(self.class_name)
        result[self.__keys__.class_docs] = str(self.class_docs)
        result[self.__keys__.class_icon] = str(self.class_icon)
        result[self.__keys__.class_color] = str(self.class_color)

        serialized_class_nodes = serialize(self.class_nodes)
        assert isinstance(serialized_class_nodes, list)
        assert all(isinstance(node, dict) for node in serialized_class_nodes)
        result[self.__keys__.class_nodes] = serialized_class_nodes

        serialized_class_arcs = serialize(self.class_arcs)
        assert isinstance(serialized_class_arcs, list)
        assert all(isinstance(node, dict) for node in serialized_class_arcs)
        result[self.__keys__.class_arcs] = serialized_class_arcs

        return result

    def __deserialize__(self, data):
        assert isinstance(data, dict)
        self.class_name = str(data.get(self.__keys__.class_name, str()))
        self.class_docs = str(data.get(self.__keys__.class_docs, str()))
        self.class_icon = str(data.get(self.__keys__.class_icon, str()))
        self.class_color = str(data.get(self.__keys__.class_color, str()))

        self.class_nodes = deserialize(
            data.get(self.__keys__.class_nodes, list()),
            List[FlowNode],
        )
        assert isinstance(self.class_nodes, list)
        assert all(isinstance(node, FlowNode) for node in self.class_nodes)

        self.class_arcs = deserialize(
            data.get(self.__keys__.class_arcs, list()),
            List[FlowArc],
        )
        assert isinstance(self.class_arcs, list)
        assert all(isinstance(node, FlowArc) for node in self.class_arcs)

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
