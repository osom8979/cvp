# -*- coding: utf-8 -*-

from typing import Final

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
