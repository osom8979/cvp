# -*- coding: utf-8 -*-

from OpenGL import GL, GLU

from cvp.context.context import Context
from cvp.gl.objects.simple.cube import draw_simple_cube


class World:
    def __init__(self, context: Context):
        self._context = context
        self._delta = 0.0

    @property
    def home(self):
        return self._context.home

    @property
    def config(self):
        return self._context.config

    @property
    def debug(self):
        return self._context.debug

    @property
    def verbose(self):
        return self._context.verbose

    def on_create(self):
        assert self

    def on_window_resized(self, x: int, y: int) -> None:
        assert self
        GLU.gluPerspective(45, (x / y), 0.1, 50.0)
        GL.glTranslatef(0.0, 0.0, -5)

    def on_destroy(self):
        assert self

    def on_process(self, delta: float):
        self._delta += delta

        if self._delta >= (1.0 / 60.0):
            self._delta -= 1.0 / 60.0
            GL.glRotatef(1, 3, 1, 1)

        draw_simple_cube()
