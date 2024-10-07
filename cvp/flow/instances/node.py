# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from typing import Optional

from cvp.flow.templates.node import FlowNode


@unique
class NodeKeys(StrEnum):
    name_ = auto()
    template = auto()


class Node:
    __template_class__ = FlowNode
    __keys__ = NodeKeys

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
