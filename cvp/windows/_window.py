# -*- coding: utf-8 -*-

from cvp.renderer.interface import WindowInterface
from cvp.types.override import override


class Window(WindowInterface):
    @override
    def on_process(self) -> None:
        pass

    @override
    def on_create(self) -> None:
        pass

    @override
    def on_destroy(self) -> None:
        pass
