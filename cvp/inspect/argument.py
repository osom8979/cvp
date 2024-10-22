# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from inspect import Parameter
from typing import Annotated, Any, Sequence, get_args, get_origin

# noinspection PyProtectedMember
from typing_extensions import _AnnotatedAlias


@unique
class ParamType(StrEnum):
    boolean = auto()
    complex = auto()
    floating = auto()
    integer = auto()
    mapping = auto()
    sequence = auto()
    string = auto()
    uri = auto()


class Argument:
    def __init__(self, param: Parameter, value=Parameter.empty):
        self._param = param
        self._value = value

    @property
    def name(self):
        return self._param.name

    @property
    def default(self):
        return self._param.default

    @property
    def annotation(self):
        return self._param.annotation

    @property
    def kind(self):
        return self._param.kind

    @property
    def value(self):
        return self._value

    @property
    def is_empty_value(self):
        return self._value == Parameter.empty

    @property
    def is_empty_default(self):
        return self._param.default == Parameter.empty

    @property
    def is_empty_annotation(self):
        return self._param.annotation == Parameter.empty

    @property
    def is_annotated(self):
        return (
            hasattr(self._param.annotation, "__metadata__")
            and isinstance(self._param.annotation, _AnnotatedAlias)
            and get_origin(self._param.annotation) == Annotated
        )

    @property
    def annotated_args(self) -> Sequence[Any]:
        if not self.is_annotated:
            if isinstance(self._param.annotation, type):
                annotation_name = self._param.annotation.__name__
            else:
                annotation_name = type(self._param.annotation).__name__
            raise TypeError(f"Parameter is not of type Annotated: {annotation_name}")

        return get_args(self._param.annotation)

    @property
    def type_deduction(self) -> type:
        if not self.is_empty_annotation:
            if self.is_annotated:
                return self.annotated_args[0]
            else:
                origin = get_origin(self._param.annotation)
                if origin is not None:
                    return origin
                else:
                    return self._param.annotation
        elif self._param.default != Parameter.empty:
            return type(self._param.default)
        else:
            return object
