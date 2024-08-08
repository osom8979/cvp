# -*- coding: utf-8 -*-

from typing import Final, List

DEFAULT_FFMPEG_RECV_FORMAT: Final[str] = (
    # global options
    "-hide_banner "
    # infile options
    "-fflags nobuffer -fflags discardcorrupt -flags low_delay -rtsp_transport tcp "
    "-i {source} "
    # outfile options
    "-f image2pipe -pix_fmt {pixel_format} -vcodec rawvideo pipe:1"
)

DEFAULT_FFMPEG_SEND_FORMAT: Final[str] = (
    # global options
    "-hide_banner "
    # infile options
    "-f rawvideo -pix_fmt {pixel_format} -s {width}x{height} -i pipe:0 "
    # outfile options
    "-c:v libx264 "
    "-preset ultrafast "
    "-crf 30 "
    "-f {file_format} {destination}"
)


class FileBuilder:
    _options: List[str]

    def __init__(self, ffmpeg: "FFmpegBuilder", file: str):
        self._ffmpeg = ffmpeg
        self._file = file
        self._options = list()

    def append_options(self, *args: str):
        self._options += args
        return self


class InputFileBuilder(FileBuilder):
    pass


class OutputFileBuilder(FileBuilder):
    pass


class FFmpegBuilder:
    """
    ffmpeg video converter

    Synopsis:
        ffmpeg [global_options] \
            {[input_file_options] -i input_url} ... \
            {[output_file_options] output_url} ...
    """

    _globals: List[str]
    _files: List[FileBuilder]

    def __init__(self, ffmpeg="ffmpeg") -> None:
        self._ffmpeg = ffmpeg
        self._globals = list()
        self._files = list()

    def append_global_options(self, *args: str):
        self._globals += args
        return self

    def hide_banner(self):
        return self.append_global_options("-hide_banner")

    def infile(self, file: str):
        builder = InputFileBuilder(ffmpeg=self, file=file)
        self._files.append(builder)
        return builder

    def outfile(self, file: str):
        builder = OutputFileBuilder(ffmpeg=self, file=file)
        self._files.append(builder)
        return builder
