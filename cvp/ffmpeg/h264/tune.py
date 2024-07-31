# -*- coding: utf-8 -*-

from enum import IntEnum, auto, unique


@unique
class Tune(IntEnum):
    """
    change settings based upon the specifics of input.

    List presets and tunes:
        `ffmpeg -hide_banner -f lavfi -i nullsrc -c:v libx264 -preset help -f mp4 -`

    References:
        https://trac.ffmpeg.org/wiki/Encode/H.264#Tune
    """

    film = auto()
    """use for high quality movie content; lowers deblocking"""

    animation = auto()
    """good for cartoons; uses higher deblocking and more reference frames"""

    grain = auto()
    """preserves the grain structure in old, grainy film material"""

    stillimage = auto()
    """good for slideshow-like content"""

    fastdecode = auto()
    """allows faster decoding by disabling certain filters"""

    zerolatency = auto()
    """good for fast encoding and low-latency streaming"""

    psnr = auto()
    """ignore this as it is only used for codec development"""

    ssim = auto()
    """ignore this as it is only used for codec development"""
