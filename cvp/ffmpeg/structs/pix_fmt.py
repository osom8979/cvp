# -*- coding: utf-8 -*-

from io import StringIO
from subprocess import check_output
from typing import Final, List, NamedTuple, Sequence

# noinspection SpellCheckingInspection
_FFMPEG_PIX_FMTS_STDOUT_SAMPLE = """
Pixel formats:
I.... = Supported Input  format for conversion
.O... = Supported Output format for conversion
..H.. = Hardware accelerated format
...P. = Paletted format
....B = Bitstream format
FLAGS NAME            NB_COMPONENTS BITS_PER_PIXEL
-----
IO... yuv420p                3            12
IO... yuyv422                3            16
IO... rgb24                  3            24
IO... bgr24                  3            24
IO... yuv422p                3            16
IO... yuv444p                3            24
IO... yuv410p                3             9
IO... yuv411p                3            12
IO... gray                   1             8
IO..B monow                  1             1
IO..B monob                  1             1
I..P. pal8                   1             8
IO... yuvj420p               3            12
IO... yuvj422p               3            16
IO... yuvj444p               3            24
IO... uyvy422                3            16
..... uyyvyy411              3            12
IO... bgr8                   3             8
.O..B bgr4                   3             4
IO... bgr4_byte              3             4
IO... rgb8                   3             8
.O..B rgb4                   3             4
IO... rgb4_byte              3             4
IO... nv12                   3            12
IO... nv21                   3            12
IO... argb                   4            32
IO... rgba                   4            32
IO... abgr                   4            32
IO... bgra                   4            32
IO... gray16be               1            16
IO... gray16le               1            16
IO... yuv440p                3            16
IO... yuvj440p               3            16
IO... yuva420p               4            20
IO... rgb48be                3            48
IO... rgb48le                3            48
IO... rgb565be               3            16
IO... rgb565le               3            16
IO... rgb555be               3            15
IO... rgb555le               3            15
IO... bgr565be               3            16
IO... bgr565le               3            16
IO... bgr555be               3            15
IO... bgr555le               3            15
..H.. vaapi_moco             0             0
..H.. vaapi_idct             0             0
..H.. vaapi_vld              0             0
IO... yuv420p16le            3            24
IO... yuv420p16be            3            24
IO... yuv422p16le            3            32
IO... yuv422p16be            3            32
IO... yuv444p16le            3            48
IO... yuv444p16be            3            48
..H.. dxva2_vld              0             0
IO... rgb444le               3            12
IO... rgb444be               3            12
IO... bgr444le               3            12
IO... bgr444be               3            12
IO... ya8                    2            16
IO... bgr48be                3            48
IO... bgr48le                3            48
IO... yuv420p9be             3            13
IO... yuv420p9le             3            13
IO... yuv420p10be            3            15
IO... yuv420p10le            3            15
IO... yuv422p10be            3            20
IO... yuv422p10le            3            20
IO... yuv444p9be             3            27
IO... yuv444p9le             3            27
IO... yuv444p10be            3            30
IO... yuv444p10le            3            30
IO... yuv422p9be             3            18
IO... yuv422p9le             3            18
IO... gbrp                   3            24
IO... gbrp9be                3            27
IO... gbrp9le                3            27
IO... gbrp10be               3            30
IO... gbrp10le               3            30
IO... gbrp16be               3            48
IO... gbrp16le               3            48
IO... yuva422p               4            24
IO... yuva444p               4            32
IO... yuva420p9be            4            22
IO... yuva420p9le            4            22
IO... yuva422p9be            4            27
IO... yuva422p9le            4            27
IO... yuva444p9be            4            36
IO... yuva444p9le            4            36
IO... yuva420p10be           4            25
IO... yuva420p10le           4            25
IO... yuva422p10be           4            30
IO... yuva422p10le           4            30
IO... yuva444p10be           4            40
IO... yuva444p10le           4            40
IO... yuva420p16be           4            40
IO... yuva420p16le           4            40
IO... yuva422p16be           4            48
IO... yuva422p16le           4            48
IO... yuva444p16be           4            64
IO... yuva444p16le           4            64
..H.. vdpau                  0             0
IO... xyz12le                3            36
IO... xyz12be                3            36
..... nv16                   3            16
..... nv20le                 3            20
..... nv20be                 3            20
IO... rgba64be               4            64
IO... rgba64le               4            64
IO... bgra64be               4            64
IO... bgra64le               4            64
IO... yvyu422                3            16
IO... ya16be                 2            32
IO... ya16le                 2            32
IO... gbrap                  4            32
IO... gbrap16be              4            64
IO... gbrap16le              4            64
..H.. qsv                    0             0
..H.. mmal                   0             0
..H.. d3d11va_vld            0             0
..H.. cuda                   0             0
IO... 0rgb                   3            24
IO... rgb0                   3            24
IO... 0bgr                   3            24
IO... bgr0                   3            24
IO... yuv420p12be            3            18
IO... yuv420p12le            3            18
IO... yuv420p14be            3            21
IO... yuv420p14le            3            21
IO... yuv422p12be            3            24
IO... yuv422p12le            3            24
IO... yuv422p14be            3            28
IO... yuv422p14le            3            28
IO... yuv444p12be            3            36
IO... yuv444p12le            3            36
IO... yuv444p14be            3            42
IO... yuv444p14le            3            42
IO... gbrp12be               3            36
IO... gbrp12le               3            36
IO... gbrp14be               3            42
IO... gbrp14le               3            42
IO... yuvj411p               3            12
I.... bayer_bggr8            3             8
I.... bayer_rggb8            3             8
I.... bayer_gbrg8            3             8
I.... bayer_grbg8            3             8
I.... bayer_bggr16le         3            16
I.... bayer_bggr16be         3            16
I.... bayer_rggb16le         3            16
I.... bayer_rggb16be         3            16
I.... bayer_gbrg16le         3            16
I.... bayer_gbrg16be         3            16
I.... bayer_grbg16le         3            16
I.... bayer_grbg16be         3            16
..H.. xvmc                   0             0
IO... yuv440p10le            3            20
IO... yuv440p10be            3            20
IO... yuv440p12le            3            24
IO... yuv440p12be            3            24
IO... ayuv64le               4            64
..... ayuv64be               4            64
..H.. videotoolbox_vld       0             0
IO... p010le                 3            15
IO... p010be                 3            15
IO... gbrap12be              4            48
IO... gbrap12le              4            48
IO... gbrap10be              4            40
IO... gbrap10le              4            40
..H.. mediacodec             0             0
IO... gray12be               1            12
IO... gray12le               1            12
IO... gray10be               1            10
IO... gray10le               1            10
IO... p016le                 3            24
IO... p016be                 3            24
..H.. d3d11                  0             0
IO... gray9be                1             9
IO... gray9le                1             9
IO... gbrpf32be              3            96
IO... gbrpf32le              3            96
IO... gbrapf32be             4            128
IO... gbrapf32le             4            128
..H.. drm_prime              0             0
..H.. opencl                 0             0
IO... gray14be               1            14
IO... gray14le               1            14
IO... grayf32be              1            32
IO... grayf32le              1            32
IO... yuva422p12be           4            36
IO... yuva422p12le           4            36
IO... yuva444p12be           4            48
IO... yuva444p12le           4            48
IO... nv24                   3            24
IO... nv42                   3            24
..H.. vulkan                 0             0
..... y210be                 3            20
I.... y210le                 3            20
IO... x2rgb10le              3            30
..... x2rgb10be              3            30
"""

FFMPEG_PIX_FMTS_HEADER_LINES: Final[Sequence[str]] = (
    "Pixel formats:",
    "I.... = Supported Input  format for conversion",
    ".O... = Supported Output format for conversion",
    "..H.. = Hardware accelerated format",
    "...P. = Paletted format",
    "....B = Bitstream format",
    "FLAGS NAME            NB_COMPONENTS BITS_PER_PIXEL",
)
"""Skip unnecessary header lines in `ffmpeg -hide_banner -pix_fmts` command."""


class PixFmt(NamedTuple):
    supported_input_format: bool
    supported_output_format: bool
    hardware_accelerated_format: bool
    paletted_format: bool
    bitstream_format: bool
    name: str
    nb_components: int
    bits_per_pixel: int

    def __repr__(self):
        buffer = StringIO()
        buffer.write("I" if self.supported_input_format else ".")
        buffer.write("O" if self.supported_output_format else ".")
        buffer.write("H" if self.hardware_accelerated_format else ".")
        buffer.write("P" if self.paletted_format else ".")
        buffer.write("B" if self.bitstream_format else ".")
        buffer.write(f" comp={self.nb_components}")
        buffer.write(f" bits={self.bits_per_pixel:<3}")
        buffer.write(f" {self.name}")
        return buffer.getvalue()

    @classmethod
    def from_format_line(cls, line: str):
        cols = [c.strip() for c in line.split()]
        assert len(cols) == 4
        flags = cols[0]
        return cls(
            supported_input_format=(flags[0] == "I"),
            supported_output_format=(flags[1] == "O"),
            hardware_accelerated_format=(flags[2] == "H"),
            paletted_format=(flags[3] == "P"),
            bitstream_format=(flags[4] == "B"),
            name=cols[1],
            nb_components=int(cols[2]),
            bits_per_pixel=int(cols[3]),
        )


def parse_fix_fmts_output(text: str) -> List[PixFmt]:
    lines = text.splitlines()
    for i, header_line in enumerate(FFMPEG_PIX_FMTS_HEADER_LINES):
        if lines[i] != header_line:
            raise ValueError(f"This is not the expected header line #{i}: '{lines[i]}'")

    begin = len(FFMPEG_PIX_FMTS_HEADER_LINES)
    lines = lines[begin:]

    # [IMPORTANT] Do not use strip
    return [PixFmt.from_format_line(line) for line in lines]


def inspect_pix_fmts(ffmpeg="ffmpeg") -> List[PixFmt]:
    cmds = (ffmpeg, "-hide_banner", "-pix_fmts")
    output = check_output(cmds).decode("utf-8")
    return parse_fix_fmts_output(output)


def find_pix_fmt(pixel_format: str, ffmpeg="ffmpeg") -> PixFmt:
    pix_fmts = inspect_pix_fmts(ffmpeg)
    filtered_pix_fmts = list(filter(lambda x: x.name == pixel_format, pix_fmts))
    if not filtered_pix_fmts:
        raise IndexError(f"Not found pixel format: {pixel_format}")
    assert len(filtered_pix_fmts) == 1
    return filtered_pix_fmts[0]


def find_bits_per_pixel(pixel_format: str, ffmpeg="ffmpeg") -> int:
    return find_pix_fmt(pixel_format, ffmpeg).bits_per_pixel
