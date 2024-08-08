# -*- coding: utf-8 -*-

from cvp.renderer.interface import WindowInterface
from cvp.types.override import override


class Window(WindowInterface):
    def __init__(self):
        self._initialized = False

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
