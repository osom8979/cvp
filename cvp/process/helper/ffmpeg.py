# -*- coding: utf-8 -*-

from typing import Final, Mapping, Optional, Sequence, Tuple, Union

from cvp.config.sections.ffmpeg import FFmpegConfig
from cvp.process.frame import FrameReaderProcess, FrameShape
from cvp.process.stream import StreamBufferPair
from cvp.resources.home import HomeDir

RGB24_CHANNELS: Final[int] = 3
PIPE_STDOUT: Final[str] = "pipe:1"


class FFmpegProcessHelper:
    def __init__(self, config: FFmpegConfig, home: HomeDir):
        self._config = config
        self._home = home

    @property
    def ffmpeg(self) -> str:
        return self._config.ffmpeg

    def _spawn(
        self,
        name: str,
        args: Sequence[str],
        frame_shape: Union[FrameShape | Tuple[int, int, int] | Sequence[int]],
        env: Optional[Union[Mapping[str, str], Mapping[bytes, bytes]]] = None,
        start_thread=True,
    ):
        stderr_path = self._home.processes.gen(name, "stderr")
        if not stderr_path.parent.is_dir():
            stderr_path.parent.mkdir(parents=True, exist_ok=True)

        stream_buffers = StreamBufferPair(
            stdout=None,
            stderr=stderr_path,
            encoding=self._config.logging_encoding,
            maxsize=self._config.logging_maxsize,
            newline_size=self._config.logging_newline_size,
        )
        assert stream_buffers.stderr is not None
        stderr_fileno = stream_buffers.stderr.writable_fileno()
        assert 0 <= stderr_fileno
        process = FrameReaderProcess(
            name=name,
            args=args,
            frame_shape=frame_shape,
            stdin=None,
            stderr=stderr_fileno,
            cwd=str(self._home),
            env=env,
            creation_flags=None,
            target=None,
            stream_buffers=stream_buffers,
        )
        if start_thread:
            process.thread.start()
        return process

    @staticmethod
    def alsa_default_args(stream_index=0) -> Sequence[str]:
        return "-map", f"{stream_index}:a", "-f", "alsa", "default"

    @staticmethod
    def directsound_default_args(stream_index=0) -> Sequence[str]:
        return "-map", f"{stream_index}:a", "-f", "directsound", "default"

    @staticmethod
    def rgb24_pipe_stdout_args(
        width: int,
        height: int,
        stream_index=0,
    ) -> Sequence[str]:
        return (
            "-map",
            f"{stream_index}:v",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            f"{width}x{height}",
            PIPE_STDOUT,
        )

    def spawn_with_file(self, key: str, file: str, width: int, height: int):
        args = (
            self.ffmpeg,
            "-hide_banner",
            "-re",
            "-i",
            file,
            *self.alsa_default_args(),
            *self.rgb24_pipe_stdout_args(width, height),
        )
        frame_shape = width, height, RGB24_CHANNELS
        return self._spawn(key, args=args, frame_shape=frame_shape)

    def spawn_with_rtsp(self, key: str, url: str, width: int, height: int):
        args = (
            self.ffmpeg,
            "-hide_banner",
            "-fflags",
            "nobuffer",
            "-fflags",
            "discardcorrupt",
            "-flags",
            "low_delay",
            "-rtsp_transport",
            "tcp",
            "-i",
            url,
            *self.rgb24_pipe_stdout_args(width, height),
        )
        frame_shape = width, height, RGB24_CHANNELS
        return self._spawn(key, args=args, frame_shape=frame_shape)
