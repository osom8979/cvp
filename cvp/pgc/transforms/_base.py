# -*- coding: utf-8 -*-

from pygame.surface import Surface

from cvp.pgc.transforms._interface import TransformInterface
from cvp.types import override


class TransformBase(TransformInterface):
    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    @override
    def transform(self, source: Surface) -> Surface:
        return source