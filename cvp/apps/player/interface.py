# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class RendererInterface(ABC):
    @abstractmethod
    def on_process(self) -> None:
        raise NotImplementedError


class WindowInterface(RendererInterface):
    @abstractmethod
    def on_create(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_destroy(self) -> None:
        raise NotImplementedError
