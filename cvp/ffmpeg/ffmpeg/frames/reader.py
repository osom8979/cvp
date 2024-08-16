# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import IO, Optional

from cvp.types.override import override


class FFmpegFrameInterface(ABC):
    @abstractmethod
    def on_frame(self, data: bytes) -> None:
        raise NotImplementedError


class FFmpegFrameReader(FFmpegFrameInterface):
    _remain: Optional[bytes]

    def __init__(self, pipe: IO[bytes], frame_size: int):
        self._pipe = pipe
        self._frame_size = frame_size
        self._remain = None

    @property
    def frame_size(self):
        return self._frame_size

    def flush(self) -> None:
        self._pipe.flush()

    def read(self) -> None:
        if self._remain:
            next_read_size = self._frame_size - len(self._remain)
            self._remain = self.on_recv(self._remain + self._pipe.read(next_read_size))
        else:
            # Sections of code with the highest probability of entry:
            self._remain = self.on_recv(self._pipe.read(self._frame_size))

    def read_eof(self) -> None:
        if self._remain:
            self._remain = self.on_recv(self._remain + self._pipe.read())
        else:
            self._remain = self.on_recv(self._pipe.read())

    def on_recv(self, data: bytes) -> Optional[bytes]:
        if len(data) == 0:
            return None

        if len(data) == self._frame_size:
            self.on_frame(data)
            return None

        assert 0 < len(data) < self._frame_size
        return data

    @override
    def on_frame(self, data: bytes) -> None:
        raise NotImplementedError
