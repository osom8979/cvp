# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from cvp.widgets.widget import WidgetInterface


class PreferenceWidget(WidgetInterface, ABC):
    @property
    @abstractmethod
    def label(self) -> str:
        raise NotImplementedError
