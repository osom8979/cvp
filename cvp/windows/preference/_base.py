# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from cvp.renderer.widget.interface import WidgetInterface


class PreferenceWidget(WidgetInterface, ABC):
    @property
    @abstractmethod
    def label(self) -> str:
        raise NotImplementedError
