# -*- coding: utf-8 -*-

from ctypes import addressof, create_string_buffer, memmove

from OpenGL import GL


class PixelBufferObject:
    def __init__(self):
        self._size = 0
        self._pbo = 0
        self._bound = False

    @property
    def opened(self) -> bool:
        return self._pbo != 0

    @property
    def bound(self) -> bool:
        return self._bound

    def open(self, size: int) -> None:
        if self._pbo != 0:
            raise ValueError("PBO is already opened")

        self._size = size
        self._pbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_PIXEL_UNPACK_BUFFER, self._pbo)
        GL.glBufferData(GL.GL_PIXEL_UNPACK_BUFFER, size, None, GL.GL_STREAM_DRAW)
        GL.glBindBuffer(GL.GL_PIXEL_UNPACK_BUFFER, 0)

    def close(self) -> None:
        if self._pbo == 0:
            raise ValueError("PBO is not opened")

        GL.glDeleteBuffers(1, self._pbo)
        self._pbo = 0

    def bind(self) -> None:
        if self._bound:
            raise ValueError("PBO is already bound")

        GL.glBindBuffer(GL.GL_PIXEL_UNPACK_BUFFER, self._pbo)
        self._bound = True

    def release(self) -> None:
        if not self._bound:
            raise ValueError("PBO is not bound")

        GL.glBindBuffer(GL.GL_PIXEL_UNPACK_BUFFER, 0)
        self._bound = False

    def __enter__(self):
        self.bind()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def update_stream_draw(self):
        assert self._bound, "PBO must be bound"

        # GL.GL_STATIC_COPY
        # GL.GL_STATIC_DRAW
        # GL.GL_STATIC_READ
        # GL.GL_STREAM_COPY
        # GL.GL_STREAM_DRAW
        # GL.GL_STREAM_READ

        GL.glBufferData(GL.GL_PIXEL_UNPACK_BUFFER, self._size, None, GL.GL_STREAM_DRAW)

    def draw_unpack_buffer(self, pixels: bytes):
        assert self._bound, "PBO must be bound"

        buffer_ptr = GL.glMapBuffer(GL.GL_PIXEL_UNPACK_BUFFER, GL.GL_WRITE_ONLY)
        if not buffer_ptr:
            raise ValueError("MapBuffer is not bound")

        try:
            pixels_ptr = addressof(create_string_buffer(pixels, self._size))
            memmove(buffer_ptr, pixels_ptr, self._size)
        finally:
            GL.glUnmapBuffer(GL.GL_PIXEL_UNPACK_BUFFER)
