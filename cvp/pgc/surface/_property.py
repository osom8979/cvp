# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from pygame.surface import Surface


class SurfacePropertyInterface(metaclass=ABCMeta):
    @property
    @abstractmethod
    def surface(self) -> Surface:
        raise NotImplementedError
