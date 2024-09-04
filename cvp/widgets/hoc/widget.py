# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from cvp.context import latest_context


class WidgetInterface(ABC):
    @abstractmethod
    def on_process(self) -> None:
        raise NotImplementedError

    @staticmethod
    def propagated_context():
        return latest_context()
