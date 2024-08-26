# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class WidgetInterface(ABC):
    @abstractmethod
    def on_process(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def do_process(self) -> None:
        raise NotImplementedError
