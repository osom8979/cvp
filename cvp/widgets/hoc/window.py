# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

# noinspection PyProtectedMember
from cvp.config.sections._window import CommonWindowSection
from cvp.types.override import override

SectionT = TypeVar("SectionT", bound=CommonWindowSection)


class WindowInterface(ABC):
    @abstractmethod
    def on_create(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_destroy(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_process(self) -> None:
        raise NotImplementedError


class Window(Generic[SectionT], WindowInterface):
    def __init__(self, section: SectionT):
        assert isinstance(section, CommonWindowSection)
        self._section = section
        self._initialized = False

    @property
    def section(self) -> SectionT:
        return self._section

    @property
    def initialized(self) -> bool:
        return self._initialized

    @property
    def opened(self) -> bool:
        return self._section.opened

    @opened.setter
    def opened(self, value: bool) -> None:
        self._section.opened = value

    @override
    def on_process(self) -> None:
        pass

    @override
    def on_create(self) -> None:
        pass

    @override
    def on_destroy(self) -> None:
        pass

    def do_process(self) -> None:
        if not self._initialized:
            self.on_create()
            self._initialized = True

        self.on_process()

    def do_create(self) -> None:
        if not self._initialized:
            self.on_create()
            self._initialized = True

    def do_destroy(self) -> None:
        if self._initialized:
            self.on_destroy()
            self._initialized = False
