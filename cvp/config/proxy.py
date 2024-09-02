# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class ValueProxy(ABC):
    @abstractmethod
    def set(self, value: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self) -> str:
        raise NotImplementedError
