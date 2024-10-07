# -*- coding: utf-8 -*-

from typing import Sequence, Union

from cvp.pygame.transforms._base import TransformBase
from cvp.pygame.types import SequenceProtocol
from cvp.types import override
from pygame.surface import Surface
from pygame.transform import smoothscale_by


class SmoothscaleByTransform(TransformBase):
    def __init__(self, factor: Union[float, Sequence[float]]):
        self.factor = factor

    @override
    def transform(self, source: Surface) -> Surface:
        assert isinstance(self.factor, SequenceProtocol)
        return smoothscale_by(source, self.factor)
