# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from typing import Optional, Union

from cvp.flow.enums.action import DEFAULT_FLOW_ACTION_VALUE as _DEFAULT_ACTION
from cvp.flow.enums.action import FlowAction, normalize_action_value
from cvp.flow.enums.stream import DEFAULT_FLOW_STREAM_VALUE as _DEFAULT_STREAM
from cvp.flow.enums.stream import FlowStream, normalize_stream_value


@unique
class FlowPinKeys(StrEnum):
    class_name = auto()
    class_docs = auto()
    class_action = auto()
    class_stream = auto()
    class_dtype = auto()
    class_required = auto()
    class_icon = auto()
    class_color = auto()


class FlowPin:
    Keys = FlowPinKeys

    def __init__(
        self,
        class_name: Optional[str] = None,
        class_docs: Optional[str] = None,
        class_action: Optional[Union[FlowAction, str, int]] = _DEFAULT_ACTION,
        class_stream: Optional[Union[FlowStream, str, int]] = _DEFAULT_STREAM,
        class_dtype: Optional[str] = None,
        class_required=False,
        class_icon: Optional[str] = None,
        class_color: Optional[str] = None,
    ):
        self.class_name = class_name if class_name else str()
        self.class_docs = class_docs if class_docs else str()
        self.class_action = normalize_action_value(class_action)
        self.class_stream = normalize_stream_value(class_stream)
        self.class_dtype = class_dtype if class_dtype else str()
        self.class_required = class_required
        self.class_icon = class_icon if class_icon else str()
        self.class_color = class_color if class_color else str()

    def __repr__(self):
        return (
            f"<{type(self).__name__} @{id(self)}"
            f" class_name='{self.class_name}'"
            f" class_docs='{self.class_docs}'"
            f" class_action={FlowAction(self.class_action).name}"
            f" class_stream={FlowStream(self.class_stream).name}"
            f" class_dtype='{self.class_dtype}'"
            f" class_required={self.class_required}"
            f" class_icon='{self.class_icon}'"
            f" class_color='{self.class_color}'>"
        )

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, type(self))
            and self.class_name == other.class_name
            and self.class_docs == other.class_docs
            and self.class_action == other.class_action
            and self.class_stream == other.class_stream
            and self.class_dtype == other.class_dtype
            and self.class_required == other.class_required
            and self.class_icon == other.class_icon
            and self.class_color == other.class_color
        )

    def __copy__(self):
        return type(self)(
            class_name=copy(self.class_name),
            class_docs=copy(self.class_docs),
            class_action=copy(self.class_action),
            class_stream=copy(self.class_stream),
            class_dtype=copy(self.class_dtype),
            class_required=copy(self.class_required),
            class_icon=copy(self.class_icon),
            class_color=copy(self.class_color),
        )

    def __deepcopy__(self, memo):
        result = type(self)(
            class_name=deepcopy(self.class_name, memo),
            class_docs=deepcopy(self.class_docs, memo),
            class_action=deepcopy(self.class_action, memo),
            class_stream=deepcopy(self.class_stream, memo),
            class_dtype=deepcopy(self.class_dtype, memo),
            class_required=deepcopy(self.class_required, memo),
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
        result[self.Keys.class_action] = int(self.class_action)
        result[self.Keys.class_stream] = int(self.class_stream)
        result[self.Keys.class_dtype] = str(self.class_dtype)
        result[self.Keys.class_required] = bool(self.class_required)
        result[self.Keys.class_icon] = str(self.class_icon)
        result[self.Keys.class_color] = str(self.class_color)
        return result

    def __deserialize__(self, data):
        assert isinstance(data, dict)
        self.class_name = str(data.get(self.Keys.class_name, str()))
        self.class_docs = str(data.get(self.Keys.class_docs, str()))
        self.class_action = int(data.get(self.Keys.class_action, _DEFAULT_ACTION))
        self.class_stream = int(data.get(self.Keys.class_stream, _DEFAULT_STREAM))
        self.class_dtype = str(data.get(self.Keys.class_dtype, str()))
        self.class_required = bool(data.get(self.Keys.class_required, False))
        self.class_icon = str(data.get(self.Keys.class_icon, str()))
        self.class_color = str(data.get(self.Keys.class_color, str()))
