# -*- coding: utf-8 -*-

from collections import OrderedDict
from inspect import Parameter
from typing import Annotated, Any, Dict, Sequence, get_args, get_origin

# noinspection PyProtectedMember
from typing_extensions import _AnnotatedAlias


class Argument:
    def __init__(self, param: Parameter, value=Parameter.empty):
        self.param = param
        self.value = value

    @classmethod
    def from_details(
        cls,
        name: str,
        kind=Parameter.POSITIONAL_OR_KEYWORD,
        default=Parameter.empty,
        annotation=Parameter.empty,
        value=Parameter.empty,
    ):
        parameter = Parameter(name, kind, default=default, annotation=annotation)
        return cls(parameter, value)

    @property
    def name(self):
        return self.param.name

    @property
    def default(self):
        return self.param.default

    @property
    def annotation(self):
        return self.param.annotation

    @property
    def kind(self):
        return self.param.kind

    @property
    def is_empty_value(self):
        return self.value == Parameter.empty

    @property
    def is_empty_default(self):
        return self.param.default == Parameter.empty

    @property
    def is_empty_annotation(self):
        return self.param.annotation == Parameter.empty

    @property
    def is_annotated(self):
        return (
            hasattr(self.param.annotation, "__metadata__")
            and isinstance(self.param.annotation, _AnnotatedAlias)
            and get_origin(self.param.annotation) == Annotated
        )

    @property
    def annotated_args(self) -> Sequence[Any]:
        if not self.is_annotated:
            if isinstance(self.param.annotation, type):
                annotation_name = self.param.annotation.__name__
            else:
                annotation_name = type(self.param.annotation).__name__
            raise TypeError(f"Parameter is not of type Annotated: {annotation_name}")

        return get_args(self.param.annotation)

    @property
    def type_deduction(self) -> type:
        if not self.is_empty_annotation:
            if self.is_annotated:
                return self.annotated_args[0]
            else:
                origin = get_origin(self.param.annotation)
                if origin is not None:
                    return origin
                else:
                    return self.param.annotation
        elif self.param.default != Parameter.empty:
            return type(self.param.default)
        else:
            return object


class ArgumentMapper(OrderedDict[str, Argument]):
    def kwargs(self) -> Dict[str, Any]:
        return {k: v.value for k, v in self.items()}
