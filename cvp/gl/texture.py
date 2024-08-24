# -*- coding: utf-8 -*-

from OpenGL import GL


class Texture:
    def __init__(self):
        self._width = 0
        self._height = 0
        self._texture = 0
        self._bound = False

    @property
    def opened(self) -> bool:
        return self._texture != 0

    @property
    def bound(self) -> bool:
        return self._bound

    def open(self, width: int, height: int) -> None:
        if self._texture != 0:
            raise ValueError("Texture is already opened")

        self._width = width
        self._height = height
        self._texture = GL.glGenTextures(1)

        GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexImage2D(
            GL.GL_TEXTURE_2D,
            0,
            GL.GL_RGB,
            width,
            height,
            0,
            GL.GL_RGB,
            GL.GL_UNSIGNED_BYTE,
            None,
        )
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    def close(self) -> None:
        if self._texture == 0:
            raise ValueError("Texture is not opened")

        GL.glDeleteTextures(1, self._texture)
        self._texture = 0

    def bind(self) -> None:
        if self._bound:
            raise ValueError("Texture is already bound")

        GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture)
        self._bound = True

    def release(self) -> None:
        if not self._bound:
            raise ValueError("Texture is not bound")

        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        self._bound = False

    def __enter__(self):
        self.bind()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
