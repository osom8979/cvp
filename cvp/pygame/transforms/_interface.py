# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from pygame.surface import Surface


class TransformInterface(metaclass=ABCMeta):
    @abstractmethod
    def transform(self, source: Surface) -> Surface:
        raise NotImplementedError
