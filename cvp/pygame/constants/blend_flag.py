# -*- coding: utf-8 -*-

from enum import IntFlag

from pygame import constants as pg_constants


class BlendFlag(IntFlag):
    NONE = pg_constants.BLENDMODE_NONE
    ADD = pg_constants.BLEND_ADD
    ALPHA_SDL2 = pg_constants.BLEND_ALPHA_SDL2
    MAX = pg_constants.BLEND_MAX
    MIN = pg_constants.BLEND_MIN
    MULT = pg_constants.BLEND_MULT
    PREMULTIPLIED = pg_constants.BLEND_PREMULTIPLIED
    RGBA_ADD = pg_constants.BLEND_RGBA_ADD
    RGBA_MAX = pg_constants.BLEND_RGBA_MAX
    RGBA_MIN = pg_constants.BLEND_RGBA_MIN
    RGBA_MULT = pg_constants.BLEND_RGBA_MULT
    RGBA_SUB = pg_constants.BLEND_RGBA_SUB
    RGB_ADD = pg_constants.BLEND_RGB_ADD
    RGB_MAX = pg_constants.BLEND_RGB_MAX
    RGB_MIN = pg_constants.BLEND_RGB_MIN
    RGB_MULT = pg_constants.BLEND_RGB_MULT
    RGB_SUB = pg_constants.BLEND_RGB_SUB
    SUB = pg_constants.BLEND_SUB
