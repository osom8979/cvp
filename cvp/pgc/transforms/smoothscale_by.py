# -*- coding: utf-8 -*-

from typing import Sequence, Union

from pygame.surface import Surface
from pygame.transform import smoothscale_by

from cvp.pgc.transforms._base import TransformBase
from cvp.pgc.types import SequenceProtocol
from cvp.types import override


class SmoothscaleByTransform(TransformBase):
    def __init__(self, factor: Union[float, Sequence[float]]):
        self.factor = factor

    @override
    def transform(self, source: Surface) -> Surface:
        assert isinstance(self.factor, SequenceProtocol)
        return smoothscale_by(source, self.factor)
