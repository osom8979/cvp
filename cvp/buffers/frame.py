# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from io import BytesIO
from typing import IO, Callable, Optional

from cvp.types.override import override


class FrameInterface(ABC):
    @abstractmethod
    def on_frame(self, data: bytes) -> None:
        raise NotImplementedError


class FrameBuffer(FrameInterface):
    _remain: Optional[bytes]

    def __init__(
        self,
        pipe: IO[bytes],
        frame_size: int,
        *,
        target: Optional[Callable[[bytes], None]] = None,
    ):
        self._pipe = pipe
        self._frame_size = frame_size
        self._target = target
        self._remain = None

    @property
    def frame_size(self):
        return self._frame_size

    def set_remain(self, value: Optional[bytes]) -> None:
        if value:
            assert 0 <= len(value) < self._frame_size
            self._remain = value
        else:
            self._remain = None

    def clear_remain(self) -> None:
        self.set_remain(None)

    @property
    def remain(self):
        return self._remain

    def flush(self) -> None:
        self._pipe.flush()

    def read(self) -> None:
        if self._remain:
            next_read_size = self._frame_size - len(self._remain)
            self._remain = self.on_recv(self._remain + self._pipe.read(next_read_size))
        else:
            # Most likely code section to hit:
            self._remain = self.on_recv(self._pipe.read(self._frame_size))

    def read_eof(self) -> None:
        remain_data = (self._remain if self._remain else bytes()) + self._pipe.read()
        remain_frame_count = len(remain_data) // self._frame_size

        if remain_frame_count >= 1:
            buffer = BytesIO(remain_data)
            for _ in range(remain_frame_count):
                result = self.on_recv(buffer.read(self._frame_size))
                assert result is None
            remain_data = buffer.read()

        self.set_remain(remain_data)

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
        if self._target is not None:
            self._target(data)
