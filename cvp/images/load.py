# -*- coding: utf-8 -*-

from os import PathLike
from typing import Any, NamedTuple, Tuple, Union

from numpy.typing import NDArray
from OpenGL import GL
from pygame import Surface, image


class TextureTuple(NamedTuple):
    texture_id: Any
    width: int
    height: int


def load_svg(filepath: Union[str, PathLike], size: Tuple[int, int]):
    return load_surface(image.load_sized_svg(filepath, size))


def load_image(filepath: Union[str, PathLike]):
    return load_surface(image.load(filepath))


def load_surface(surface: Surface):
    width, height = surface.get_size()
    image_data = image.tobytes(surface, "RGBA")
    return create_texture(width, height, image_data)


def load_rgba_array(array: NDArray):
    assert len(array.shape) == 3
    assert array.shape[2] == 4
    width = array.shape[1]
    height = array.shape[0]
    image_data = array.tobytes()
    return create_texture(width, height, image_data)


def create_texture(width: int, height: int, rgba_data: bytes):
    texture_id = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexImage2D(
        GL.GL_TEXTURE_2D,
        0,
        GL.GL_RGBA,
        width,
        height,
        0,
        GL.GL_RGBA,
        GL.GL_UNSIGNED_BYTE,
        rgba_data,
    )
    GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    return TextureTuple(texture_id, width, height)
