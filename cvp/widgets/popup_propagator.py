# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Sequence

from cvp.widgets.popup import Popup


class PopupPropagator(ABC):
    @property
    @abstractmethod
    def popups(self) -> Sequence[Popup]:
        raise NotImplementedError
