# -*- coding: utf-8 -*-

from os import PathLike
from typing import Optional, Union

from cvp.buffers.lines import LinesBuffer
from cvp.types.override import override


class StreamBuffer(LinesBuffer):
    def __init__(
        self,
        path: Union[str, PathLike[str]],
        encoding="utf-8",
        maxsize: Optional[int] = None,
        newline_size: Optional[int] = None,
    ):
        super().__init__(
            path=path,
            encoding=encoding,
            maxsize=maxsize,
            newline_size=newline_size,
        )
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
    stdout: Optional[StreamBuffer]
    stderr: Optional[StreamBuffer]

    def __init__(
        self,
        stdout: Optional[Union[str, PathLike[str]]] = None,
        stderr: Optional[Union[str, PathLike[str]]] = None,
        encoding="utf-8",
        maxsize: Optional[int] = None,
        newline_size: Optional[int] = None,
    ):
        self.stdout = None
        self.stderr = None
        if stdout is not None:
            self.stdout = StreamBuffer(
                path=stdout,
                encoding=encoding,
                maxsize=maxsize,
                newline_size=newline_size,
            )
        if stderr is not None:
            self.stderr = StreamBuffer(
                path=stderr,
                encoding=encoding,
                maxsize=maxsize,
                newline_size=newline_size,
            )

    def close(self):
        if self.stdout is not None:
            self.stdout.close()
        if self.stderr is not None:
            self.stderr.close()
