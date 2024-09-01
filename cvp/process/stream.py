# -*- coding: utf-8 -*-

from os import PathLike
from typing import Optional, Union

from cvp.buffers.lines import LinesBuffer
from cvp.types import override


class StreamBuffer(LinesBuffer):
    def __init__(
        self,
        path: Union[str, PathLike[str]],
        maxlen: Optional[int] = None,
        encoding="utf-8",
    ):
        super().__init__(path, maxlen=maxlen, encoding=encoding)
        self.writable = open(path, "wb")
        try:
            self.open()
        except:  # noqa
            self.writable.close()

    def writable_fileno(self) -> int:
        return self.writable.fileno()

    def readable_fileno(self) -> Optional[int]:
        return self._file.fileno() if self._file is not None else None

    @override
    def close(self) -> None:
        super().close()
        self.writable.close()


class StreamBufferPair:
    def __init__(
        self,
        stdout: Optional[Union[str, PathLike[str]]] = None,
        stderr: Optional[Union[str, PathLike[str]]] = None,
        maxlen: Optional[int] = None,
        encoding="utf-8",
    ):
        self.stdout = StreamBuffer(stdout, maxlen, encoding) if stdout else None
        self.stderr = StreamBuffer(stderr, maxlen, encoding) if stderr else None

    def close(self):
        if self.stdout is not None:
            self.stdout.close()
        if self.stderr is not None:
            self.stderr.close()
