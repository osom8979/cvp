# -*- coding: utf-8 -*-

from typing import Generic, TypeVar

# noinspection PyProtectedMember
from cvp.config.sections._window import CommonWindowSection
from cvp.renderer.interface import WindowInterface
from cvp.types.override import override

SectionT = TypeVar("SectionT", bound=CommonWindowSection)


class Window(Generic[SectionT], WindowInterface):
    def __init__(self, config: SectionT):
        assert isinstance(config, CommonWindowSection)
        self._config = config
        self._initialized = False

    @property
    def config(self) -> SectionT:
        return self._config

    @property
    def initialized(self) -> bool:
        return self._initialized

    @override
    def on_process(self) -> None:
        pass

    @override
    def on_create(self) -> None:
        pass

    @override
    def on_destroy(self) -> None:
        pass

    @property
    def opened(self) -> bool:
        return self._config.opened

    @opened.setter
    def opened(self, value: bool) -> None:
        self._config.opened = value

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
