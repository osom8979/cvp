# -*- coding: utf-8 -*-

from abc import ABC

from cvp.pygame.surface.drawable import Drawable
from cvp.pygame.surface.gfxdrawable import GfxDrawable
from cvp.pygame.surface.imageable import Imageable
from cvp.pygame.surface.surfaceable import Surfaceable
from cvp.pygame.surface.transformable import Transformable


class SurfaceMixin(Drawable, GfxDrawable, Imageable, Surfaceable, Transformable, ABC):
    pass
