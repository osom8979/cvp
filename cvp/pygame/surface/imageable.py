# -*- coding: utf-8 -*-

from abc import ABC
from typing import Sequence, Union

from pygame import BufferProxy
from pygame import image as pg_image

from cvp.pygame.literals import FromStringFormat, ToStringFormat
from cvp.pygame.surface._property import SurfacePropertyInterface
from cvp.pygame.types import FileArg, SequenceProtocol


class Imageable(SurfacePropertyInterface, ABC):
    @staticmethod
    def image_load(file: FileArg, namehint=""):
        return pg_image.load(file, namehint)

    @staticmethod
    def image_load_sized_svg(file: FileArg, size: Sequence[float]):
        assert isinstance(size, SequenceProtocol)
        return pg_image.load_sized_svg(file, size)

    def image_save(self, file: FileArg, namehint=""):
        return pg_image.save(self.surface, file, namehint)

    @staticmethod
    def image_get_sdl_image_version(linked=True):
        return pg_image.get_sdl_image_version(linked)

    @staticmethod
    def image_get_extended():
        return pg_image.get_extended()

    def image_to_string(self, fmt: ToStringFormat, flipped=False):
        return pg_image.tostring(self.surface, fmt, flipped)

    def image_to_bytes(self, fmt: ToStringFormat, flipped=False):
        return pg_image.tobytes(self.surface, fmt, flipped)

    @staticmethod
    def image_from_string(
        data: bytes,
        size: Sequence[int],
        fmt: FromStringFormat,
        flipped=False,
        pitch=-1,
    ):
        assert isinstance(size, SequenceProtocol)
        return pg_image.fromstring(data, size, fmt, flipped, pitch)

    @staticmethod
    def image_from_bytes(
        data: bytes,
        size: Sequence[int],
        fmt: FromStringFormat,
        flipped=False,
        pitch=-1,
    ):
        assert isinstance(size, SequenceProtocol)
        return pg_image.frombytes(data, size, fmt, flipped, pitch)

    @staticmethod
    def image_from_buffer(
        data: Union[BufferProxy, bytes, bytearray, memoryview],
        size: Sequence[int],
        fmt: FromStringFormat,
        pitch=-1,
    ):
        assert isinstance(size, SequenceProtocol)
        return pg_image.frombuffer(data, size, fmt, pitch)

    @staticmethod
    def image_load_basic(file: FileArg):
        return pg_image.load_basic(file)

    @staticmethod
    def image_load_extended(file: FileArg, namehint=""):
        return pg_image.load_extended(file, namehint)

    def image_save_extended(self, file: FileArg, namehint=""):
        return pg_image.save_extended(self.surface, file, namehint)
