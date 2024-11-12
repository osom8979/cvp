# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Sequence

from cvp.renderer.popup.base import PopupBase


class PopupPropagator(ABC):
    @property
    @abstractmethod
    def popups(self) -> Sequence[PopupBase]:
        raise NotImplementedError
