# -*- coding: utf-8 -*-

from abc import abstractmethod
from enum import StrEnum, auto, unique

from cvp.config.sections.mixins._base import SupportsBaseSection


@unique
class BaseWindowKeys(StrEnum):
    opened = auto()
    title_ = "title"


class WindowMixin(SupportsBaseSection):
    @property
    @abstractmethod
    def has_opened(self) -> bool:
        return self.has(BaseWindowKeys.opened)

    @property
    @abstractmethod
    def opened(self) -> bool:
        return self.get(BaseWindowKeys.opened, False)

    @opened.setter
    @abstractmethod
    def opened(self, value: bool) -> None:
        self.set(BaseWindowKeys.opened, value)

    @property
    @abstractmethod
    def has_title(self) -> bool:
        return self.has(BaseWindowKeys.title_)

    @property
    @abstractmethod
    def title(self) -> str:
        return self.get(BaseWindowKeys.title_, str())

    @title.setter
    @abstractmethod
    def title(self, value: str) -> None:
        self.set(BaseWindowKeys.title_, value)
