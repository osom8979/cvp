# -*- coding: utf-8 -*-

from enum import IntFlag

from pygame import constants as pg_constants


class DisplayFlag(IntFlag):
    FULLSCREEN = pg_constants.FULLSCREEN
    """create a fullscreen display"""

    DOUBLEBUF = pg_constants.DOUBLEBUF
    """only applicable with OPENGL"""

    HWSURFACE = pg_constants.HWSURFACE
    """(obsolete in pygame 2) hardware accelerated, only in FULLSCREEN"""

    OPENGL = pg_constants.OPENGL
    """create an OpenGL-renderable display"""

    RESIZABLE = pg_constants.RESIZABLE
    """display window should be sizeable"""

    NOFRAME = pg_constants.NOFRAME
    """display window will have no border or controls"""

    SCALED = pg_constants.SCALED
    """resolution depends on desktop size and scale graphics"""

    SHOWN = pg_constants.SHOWN
    """window is opened in visible mode (default)"""

    HIDDEN = pg_constants.HIDDEN
    """window is opened in hidden mode"""
