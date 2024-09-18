# -*- coding: utf-8 -*-

from os import PathLike
from typing import IO, Callable, Tuple, TypeVar, Union

from typing_extensions import Protocol
from typing_extensions import SupportsIndex as SupportsIndex

AnyPath = Union[str, bytes, PathLike[str], PathLike[bytes]]
FileArg = Union[AnyPath, IO[bytes], IO[str]]

_T = TypeVar("_T", covariant=True)


class Sequence(Protocol[_T]):
    def __getitem__(self, __i: SupportsIndex) -> _T: ...
    def __len__(self) -> int: ...


Coordinate = Sequence[float]
IntCoordinate = Sequence[int]

RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[int, str, Sequence[int]]

_CanBeRect = Sequence[Union[float, Coordinate]]


class _HasRectAttribute(Protocol):
    rect: Union["RectValue", Callable[[], "RectValue"]]


RectValue = Union[_CanBeRect, _HasRectAttribute]
