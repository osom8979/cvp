# -*- coding: utf-8 -*-

from pygame import version as pg_version


class Versionable:
    @staticmethod
    def version_ver():
        return pg_version.ver

    @staticmethod
    def version_vernum():
        return pg_version.vernum

    @staticmethod
    def version_rev():
        return pg_version.rev

    @staticmethod
    def version_sdl():
        return pg_version.SDL
