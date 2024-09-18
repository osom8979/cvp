# -*- coding: utf-8 -*-

from abc import ABC

from cvp.pgc.surface.drawable import Drawable
from cvp.pgc.surface.gfxdrawable import GfxDrawable
from cvp.pgc.surface.imageable import Imageable
from cvp.pgc.surface.surfaceable import Surfaceable
from cvp.pgc.surface.transformable import Transformable


class SurfaceMixin(Drawable, GfxDrawable, Imageable, Surfaceable, Transformable, ABC):
    pass
