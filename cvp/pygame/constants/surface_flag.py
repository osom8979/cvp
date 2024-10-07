# -*- coding: utf-8 -*-

from enum import IntFlag

from pygame import constants as pg_constants


class SurfaceFlag(IntFlag):
    HWSURFACE = pg_constants.HWSURFACE
    """(obsolete in pygame 2) creates the image in video memory"""

    SRCALPHA = pg_constants.SRCALPHA
    """the pixel format will include a per-pixel alpha"""
