# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from typing import Optional


@unique
class FlowArcKeys(StrEnum):
    class_name = auto()
    class_docs = auto()
    class_icon = auto()
    class_color = auto()


class FlowArc:
    Keys = FlowArcKeys

    def __init__(
        self,
        class_name: Optional[str] = None,
        class_docs: Optional[str] = None,
        class_icon: Optional[str] = None,
        class_color: Optional[str] = None,
    ):
        self.class_name = class_name if class_name else str()
        self.class_docs = class_docs if class_docs else str()
        self.class_icon = class_icon if class_icon else str()
        self.class_color = class_color if class_color else str()

    def __repr__(self):
        return (
            f"<{type(self).__name__} @{id(self)}"
            f" class_name='{self.class_name}'"
            f" class_docs='{self.class_docs}'"
            f" class_icon='{self.class_icon}'"
            f" class_color='{self.class_color}'>"
        )

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, type(self))
            and self.class_name == other.class_name
            and self.class_docs == other.class_docs
            and self.class_icon == other.class_icon
            and self.class_color == other.class_color
        )

    def __copy__(self):
        return type(self)(
            class_name=copy(self.class_name),
            class_docs=copy(self.class_docs),
            class_icon=copy(self.class_icon),
            class_color=copy(self.class_color),
        )

    def __deepcopy__(self, memo):
        result = type(self)(
            class_name=deepcopy(self.class_name, memo),
            class_docs=deepcopy(self.class_docs, memo),
            class_icon=deepcopy(self.class_icon, memo),
            class_color=deepcopy(self.class_color, memo),
        )
        assert isinstance(memo, dict)
        memo[id(self)] = result
        return result

    def __serialize__(self):
        result = dict()
        result[self.Keys.class_name] = str(self.class_name)
        result[self.Keys.class_docs] = str(self.class_docs)
        result[self.Keys.class_icon] = str(self.class_icon)
        result[self.Keys.class_color] = str(self.class_color)
        return result

    def __deserialize__(self, data):
        assert isinstance(data, dict)
        self.class_name = str(data.get(self.Keys.class_name, str()))
        self.class_docs = str(data.get(self.Keys.class_docs, str()))
        self.class_icon = str(data.get(self.Keys.class_icon, str()))
        self.class_color = str(data.get(self.Keys.class_color, str()))
